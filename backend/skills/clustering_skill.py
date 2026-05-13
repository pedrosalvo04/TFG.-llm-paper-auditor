"""Skill de clustering semántico de papers del SOTA"""
import numpy as np
from typing import Any, Dict, List
from backend.skills.base_skill import BaseSkill


# Paleta de etiquetas para clusters (máx. 8 clusters)
_CLUSTER_COLORS = [
    "#6366f1",  # indigo
    "#10b981",  # emerald
    "#f59e0b",  # amber
    "#ef4444",  # red
    "#8b5cf6",  # violet
    "#14b8a6",  # teal
    "#f97316",  # orange
    "#ec4899",  # pink
]

_CLUSTER_EMOJIS = ["🔵", "🟢", "🟡", "🔴", "🟣", "🩵", "🟠", "🩷"]


class PaperClusteringSkill(BaseSkill):
    """
    Skill para análisis de similitud y clustering semántico de papers SOTA.

    Pasos:
    1. Embebe los abstracts con `all-MiniLM-L6-v2` (ligero, ~80 MB).
    2. Calcula la similitud coseno de cada SOTA paper contra el paper del usuario.
    3. Calcula la matriz de similitud coseno N×N entre los propios SOTA papers
       (usada internamente para KMeans y el diversity score).
    4. Aplica KMeans para agrupar papers en familias temáticas.
    5. Anota cada paper con su cluster_id, cluster_label, cluster_color,
       intra_cluster_similarity y user_similarity.
    """

    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analiza similitud y agrupa los papers recuperados.

        Args:
            context: Debe contener 'sota_papers'. Opcionalmente 'paper_text'
                     para calcular similitud contra el paper del usuario.

        Returns:
            Diccionario con:
              - 'sota_papers'         : papers enriquecidos con info de cluster y user_similarity
              - 'user_similarities'   : lista [{"title": ..., "similarity": float}] ordenada desc
              - 'diversity_score'     : float [0-1]
              - 'cluster_summary'     : dict cluster_id -> {label, color, emoji, paper_titles}
        """
        if not self.validate_context(context, ["sota_papers"]):
            return self._empty_result(context.get("sota_papers", []))

        sota_papers: List[Dict] = context["sota_papers"]
        paper_text: str = context.get("paper_text", "")

        if len(sota_papers) < 2:
            self.log_execution("⚠️ Menos de 2 papers: clustering omitido", level="warning")
            return self._empty_result(sota_papers)

        self.log_execution(f"🧮 Iniciando clustering de {len(sota_papers)} papers...")

        # --- 1. Preparar textos ---
        # SOTA papers: abstract o título como fallback
        sota_texts = [
            (p.get("abstract") or p.get("title") or "").strip()[:512]
            for p in sota_papers
        ]
        # Paper del usuario: primeros 1500 chars (cubre abstract + inicio intro)
        user_text = paper_text.strip()[:1500] if paper_text else ""

        # --- 2. Embeddings ---
        try:
            from sentence_transformers import SentenceTransformer
            self.log_execution("📥 Cargando modelo all-MiniLM-L6-v2...")
            model = SentenceTransformer("all-MiniLM-L6-v2")

            all_texts = sota_texts + ([user_text] if user_text else [])
            all_embeddings = model.encode(
                all_texts, show_progress_bar=False, normalize_embeddings=True
            )
            embeddings = all_embeddings[: len(sota_texts)]
            user_embedding = all_embeddings[len(sota_texts)] if user_text else None
            self.log_execution("✅ Embeddings generados")
        except Exception as e:
            self.log_execution(f"❌ Error generando embeddings: {e}", level="error")
            return self._empty_result(sota_papers)

        # --- 3. Similitud usuario ↔ cada SOTA paper ---
        user_sims: List[float] = []
        if user_embedding is not None:
            from sklearn.metrics.pairwise import cosine_similarity as cos_sim
            user_sims = cos_sim(
                user_embedding.reshape(1, -1), embeddings
            )[0].tolist()
            self.log_execution("✅ Similitud usuario↔SOTA calculada")
        else:
            user_sims = [0.0] * len(sota_papers)
            self.log_execution("⚠️ Sin paper_text: similitudes a 0", level="warning")

        # --- 4. Matriz coseno N×N entre SOTA papers (para clustering) ---
        try:
            from sklearn.metrics.pairwise import cosine_similarity
            sim_matrix: np.ndarray = cosine_similarity(embeddings)
            self.log_execution("✅ Matriz N×N calculada")
        except Exception as e:
            self.log_execution(f"❌ Error calculando matriz: {e}", level="error")
            return self._empty_result(sota_papers)

        # --- 5. Diversity score ---
        n = len(sota_papers)
        mask = ~np.eye(n, dtype=bool)
        mean_sim = float(sim_matrix[mask].mean())
        diversity_score = round(1.0 - mean_sim, 3)
        self.log_execution(
            f"📊 Diversidad: {diversity_score:.3f} (0=idéntico, 1=máx. diverso)"
        )

        # --- 6. KMeans clustering ---
        n_clusters = _determine_n_clusters(n)
        try:
            from sklearn.cluster import KMeans
            km = KMeans(n_clusters=n_clusters, random_state=42, n_init="auto")
            labels: np.ndarray = km.fit_predict(embeddings)
            self.log_execution(f"✅ KMeans con {n_clusters} clusters")
        except Exception as e:
            self.log_execution(f"❌ Error en KMeans: {e}", level="error")
            labels = np.zeros(n, dtype=int)

        # --- 7. Etiquetar papers (rellena paper_titles) ---
        cluster_summary: Dict[int, Dict] = {}
        for cid in range(n_clusters):
            cluster_summary[cid] = {
                "label": f"Cluster {cid + 1}",  # placeholder; se renombra abajo
                "color": _CLUSTER_COLORS[cid % len(_CLUSTER_COLORS)],
                "emoji": _CLUSTER_EMOJIS[cid % len(_CLUSTER_EMOJIS)],
                "paper_titles": [],
            }

        # Primera pasada: recoger títulos por cluster
        for i, paper in enumerate(sota_papers):
            cid = int(labels[i])
            cluster_summary[cid]["paper_titles"].append(paper.get("title", ""))

        # --- 7b. Nombrar clusters con el LLM ---
        self._name_clusters(cluster_summary)

        # Segunda pasada: enriquecer papers con metadatos de cluster
        enriched_papers = []
        for i, paper in enumerate(sota_papers):
            cid = int(labels[i])
            same_cluster = [j for j in range(n) if labels[j] == cid and j != i]
            intra_sim = (
                float(np.mean([sim_matrix[i][j] for j in same_cluster]))
                if same_cluster else 1.0
            )
            enriched = {
                **paper,
                "cluster_id": cid,
                "cluster_label": cluster_summary[cid]["label"],
                "cluster_color": cluster_summary[cid]["color"],
                "cluster_emoji": cluster_summary[cid]["emoji"],
                "intra_cluster_similarity": round(intra_sim, 3),
                "user_similarity": round(float(user_sims[i]), 3),
            }
            enriched_papers.append(enriched)


        # Lista ordenada por similitud con el usuario (para la UI)
        user_similarities = sorted(
            [
                {
                    "title": p.get("title", f"Paper {i+1}"),
                    "similarity": round(float(user_sims[i]), 3),
                    "cluster_color": cluster_summary[int(labels[i])]["color"],
                    "cluster_emoji": cluster_summary[int(labels[i])]["emoji"],
                    "cluster_label": cluster_summary[int(labels[i])]["label"],
                }
                for i, p in enumerate(sota_papers)
            ],
            key=lambda x: x["similarity"],
            reverse=True,
        )

        self.log_execution("✅ Clustering completado")
        return {
            "sota_papers": enriched_papers,
            "user_similarities": user_similarities,
            "diversity_score": diversity_score,
            "cluster_summary": cluster_summary,
        }

    def _empty_result(self, sota_papers: List[Dict]) -> Dict[str, Any]:
        return {
            "sota_papers": sota_papers,
            "user_similarities": [],
            "diversity_score": None,
            "cluster_summary": {},
        }

    def _name_clusters(self, cluster_summary: Dict[int, Dict]) -> None:
        """
        Pide al LLM que genere un nombre descriptivo (3-5 palabras en inglés)
        para cada cluster, basándose en los títulos de los papers que contiene.
        Modifica cluster_summary in-place. Fallback silencioso si no hay LLM.
        """
        if not self.llm_client:
            self.log_execution("⚠️ Sin LLM: clusters sin nombre descriptivo", level="warning")
            return

        # Construir descripción de cada cluster para el prompt
        clusters_text = "\n".join([
            f"Cluster {cid + 1}:\n" + "\n".join(f"  - {t}" for t in info["paper_titles"][:6])
            for cid, info in sorted(cluster_summary.items())
        ])

        prompt = (
            "You are a research librarian.\n\n"
            "Below are groups of academic paper titles. "
            "For each group, generate a SHORT thematic name (3-5 words, in English, "
            "technical and descriptive) that captures the common research thread.\n\n"
            f"{clusters_text}\n\n"
            "Return ONLY a valid JSON object (no markdown):\n"
            '{"1": "name for cluster 1", "2": "name for cluster 2", ...}'
        )

        try:
            response = self.llm_client.generate(prompt)
            names_raw = self.parse_json_response(response.text)

            if isinstance(names_raw, dict):
                for cid, info in cluster_summary.items():
                    # El LLM devuelve claves 1-based como strings
                    name = names_raw.get(str(cid + 1)) or names_raw.get(cid + 1)
                    if name and isinstance(name, str) and name.strip():
                        info["label"] = name.strip()
                self.log_execution("✅ Clusters nombrados por el LLM")
            else:
                self.log_execution("⚠️ Respuesta LLM inesperada para nombres de clusters", level="warning")

        except Exception as e:
            self.log_execution(f"⚠️ Error nombrando clusters: {e} — usando nombres por defecto", level="warning")


# ---------------------------------------------------------------------------
def _determine_n_clusters(n_papers: int) -> int:
    if n_papers <= 4:
        return 2
    if n_papers <= 8:
        return 3
    if n_papers <= 15:
        return 4
    if n_papers <= 25:
        return 5
    return 6
