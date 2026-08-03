from __future__ import annotations

import sqlite3
from pathlib import Path

import networkx as nx
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "database" / "openai_abuse_investigator_synthetic.sqlite"

NAVY = "#14304B"
GOLD = "#B0771A"
PALE_BLUE = "#EAF0F5"
PALE_GOLD = "#F5EEDD"
DARK = "#20262B"


st.set_page_config(
    page_title="Abuse Investigation Portfolio",
    page_icon="🔎",
    layout="wide",
)

st.markdown(
    """
    <style>
    .main-title {color:#14304B; font-size:2.3rem; font-weight:800; margin-bottom:0.1rem;}
    .subtitle {color:#B0771A; font-size:1.1rem; font-weight:700;}
    .notice {background:#F5EEDD; color:#14304B; padding:0.8rem 1rem; border-left:5px solid #B0771A;
             border-radius:0.25rem; margin:0.8rem 0 1.1rem 0;}
    .metric-label {color:#586572; font-size:0.85rem;}
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data
def read_table(table_name: str) -> pd.DataFrame:
    if not DB_PATH.exists():
        raise FileNotFoundError(f"Database not found: {DB_PATH}")
    with sqlite3.connect(DB_PATH) as connection:
        return pd.read_sql_query(f'SELECT * FROM "{table_name}"', connection)


@st.cache_data
def run_query(query: str) -> pd.DataFrame:
    with sqlite3.connect(DB_PATH) as connection:
        return pd.read_sql_query(query, connection)


def case_network(case_links: pd.DataFrame, selected_case: str | None = None) -> go.Figure:
    graph = nx.Graph()
    for row in case_links.itertuples(index=False):
        graph.add_edge(
            row.case_id_a,
            row.case_id_b,
            strength=float(row.strength),
            link_type=row.link_type,
        )

    positions = nx.spring_layout(graph, seed=42, weight="strength")
    edge_x: list[float | None] = []
    edge_y: list[float | None] = []

    for source, target in graph.edges():
        x0, y0 = positions[source]
        x1, y1 = positions[target]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    edge_trace = go.Scatter(
        x=edge_x,
        y=edge_y,
        mode="lines",
        line={"width": 1.5, "color": "#9AA8B4"},
        hoverinfo="none",
    )

    node_x = []
    node_y = []
    node_text = []
    node_colors = []
    node_sizes = []

    for node in graph.nodes():
        x, y = positions[node]
        node_x.append(x)
        node_y.append(y)
        node_text.append(f"{node}<br>Direct links: {graph.degree(node)}")
        if selected_case and node == selected_case:
            node_colors.append(GOLD)
            node_sizes.append(30)
        else:
            node_colors.append(NAVY)
            node_sizes.append(22)

    node_trace = go.Scatter(
        x=node_x,
        y=node_y,
        mode="markers+text",
        text=list(graph.nodes()),
        textposition="top center",
        hovertext=node_text,
        hoverinfo="text",
        marker={
            "size": node_sizes,
            "color": node_colors,
            "line": {"width": 2, "color": "#FFFFFF"},
        },
    )

    figure = go.Figure(data=[edge_trace, node_trace])
    figure.update_layout(
        showlegend=False,
        margin={"l": 10, "r": 10, "t": 30, "b": 10},
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        xaxis={"visible": False},
        yaxis={"visible": False},
        height=540,
    )
    return figure


st.markdown('<div class="main-title">Abuse Investigation & Detection Portfolio</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Synthetic investigations • SQL • Python • Codex-assisted workflows • Cross-case analysis</div>',
    unsafe_allow_html=True,
)
st.markdown(
    """
    <div class="notice">
    <b>Independent synthetic portfolio:</b> All cases, users, targets, devices, content, and events are fictional.
    This project is not affiliated with or endorsed by OpenAI. Automated findings require human validation.
    </div>
    """,
    unsafe_allow_html=True,
)

cases = read_table("cases")
accounts = read_table("accounts")
events = read_table("events")
content = read_table("content")
sessions = read_table("sessions")
actions = read_table("reports_enforcement")
case_links = read_table("case_links")
case_accounts = read_table("case_accounts")

for numeric_col in ["raw_risk_score"]:
    events[numeric_col] = pd.to_numeric(events[numeric_col], errors="coerce")
actions["triage_minutes"] = pd.to_numeric(actions["triage_minutes"], errors="coerce")
case_links["strength"] = pd.to_numeric(case_links["strength"], errors="coerce")
case_links["evidence_count"] = pd.to_numeric(case_links["evidence_count"], errors="coerce")

tabs = st.tabs(
    ["Executive Overview", "Case Explorer", "Cross-Case Network", "SQL Findings", "Methodology"]
)

with tabs[0]:
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Synthetic Cases", f"{len(cases):,}")
    col2.metric("Accounts", f"{len(accounts):,}")
    col3.metric("Activity Events", f"{len(events):,}")
    col4.metric("Cross-Case Links", f"{len(case_links):,}")

    left, right = st.columns([1, 1])
    with left:
        severity = cases.groupby("severity", as_index=False).size()
        severity["severity"] = pd.Categorical(
            severity["severity"], ["Critical", "High", "Control"], ordered=True
        )
        severity = severity.sort_values("severity")
        fig = px.bar(
            severity,
            x="severity",
            y="size",
            title="Case Severity",
            labels={"severity": "Severity", "size": "Cases"},
        )
        fig.update_traces(marker_color=[GOLD, NAVY, "#668A6B"])
        fig.update_layout(showlegend=False, height=350)
        st.plotly_chart(fig, use_container_width=True)

    with right:
        abuse_mix = cases.groupby("primary_abuse_type", as_index=False).size()
        fig = px.pie(
            abuse_mix,
            names="primary_abuse_type",
            values="size",
            title="Investigation Portfolio Mix",
            hole=0.45,
        )
        fig.update_layout(height=350)
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Portfolio-Level Analytical Indicators")
    indicators = pd.DataFrame(
        {
            "Indicator": [
                "Median critical-case triage time",
                "Accounts linked to more than one case",
                "Shared devices appearing across cases",
                "Content hashes reused across cases",
            ],
            "Result": [
                f"{actions.merge(cases[['case_id','severity']], on='case_id').query('severity == \"Critical\"')['triage_minutes'].median():.0f} minutes",
                str(
                    case_accounts.groupby("account_id")["case_id"]
                    .nunique()
                    .gt(1)
                    .sum()
                ),
                str(
                    sessions.merge(events[["session_id", "case_id"]], on="session_id")
                    .groupby("device_id")["case_id"]
                    .nunique()
                    .gt(1)
                    .sum()
                ),
                str(
                    content.groupby("content_hash")["case_id"]
                    .nunique()
                    .gt(1)
                    .sum()
                ),
            ],
        }
    )
    st.dataframe(indicators, use_container_width=True, hide_index=True)

with tabs[1]:
    selected_case = st.selectbox(
        "Select a synthetic investigation",
        cases["case_id"].tolist(),
        format_func=lambda case_id: (
            f"{case_id} — "
            f"{cases.loc[cases['case_id'] == case_id, 'case_title'].iloc[0]}"
        ),
    )

    case = cases.loc[cases["case_id"] == selected_case].iloc[0]
    case_events = events.loc[events["case_id"] == selected_case].copy()
    case_actions = actions.loc[actions["case_id"] == selected_case].copy()
    case_accounts_selected = case_accounts.loc[
        case_accounts["case_id"] == selected_case, "account_id"
    ].nunique()

    st.markdown(f"## {case['case_id']}: {case['case_title']}")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Severity", case["severity"])
    c2.metric("Accounts", int(case_accounts_selected))
    c3.metric("Events", len(case_events))
    c4.metric("Average Risk Score", f"{case_events['raw_risk_score'].mean():.2f}")

    st.markdown("### Case Summary")
    st.write(case["summary"])
    st.markdown(f"**Ground truth:** {case['ground_truth_label']}")
    st.markdown(f"**Pattern set:** {case['pattern_ids']}")
    st.markdown(f"**Analytical confidence:** {case['analyst_confidence']}")

    left, right = st.columns([1.35, 1])
    with left:
        timeline = (
            case_events.assign(
                timestamp=pd.to_datetime(case_events["timestamp"], utc=True, errors="coerce")
            )
            .dropna(subset=["timestamp"])
            .set_index("timestamp")
            .resample("3h")
            .size()
            .reset_index(name="events")
        )
        fig = px.line(
            timeline,
            x="timestamp",
            y="events",
            markers=True,
            title="Activity Timeline — 3-Hour Buckets",
        )
        fig.update_traces(line_color=NAVY, marker_color=GOLD)
        st.plotly_chart(fig, use_container_width=True)

    with right:
        event_mix = case_events.groupby("event_type", as_index=False).size()
        fig = px.bar(
            event_mix,
            x="size",
            y="event_type",
            orientation="h",
            title="Event Types",
            labels={"size": "Events", "event_type": "Event Type"},
        )
        fig.update_traces(marker_color=NAVY)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("### Triage and Enforcement Record")
    st.dataframe(
        case_actions[
            [
                "action_id",
                "account_id",
                "report_source",
                "triage_minutes",
                "action_type",
                "human_validated",
            ]
        ],
        use_container_width=True,
        hide_index=True,
    )

with tabs[2]:
    selected_network_case = st.selectbox(
        "Highlight a case",
        ["None"] + cases["case_id"].tolist(),
        key="network_case",
    )
    st.plotly_chart(
        case_network(
            case_links,
            None if selected_network_case == "None" else selected_network_case,
        ),
        use_container_width=True,
    )

    st.subheader("Direct Case Relationships")
    st.dataframe(
        case_links.sort_values(["strength", "evidence_count"], ascending=False),
        use_container_width=True,
        hide_index=True,
    )

with tabs[3]:
    query_options = {
        "Cross-case accounts": """
            SELECT account_id,
                   COUNT(DISTINCT case_id) AS case_count,
                   GROUP_CONCAT(DISTINCT case_id) AS cases
            FROM case_accounts
            GROUP BY account_id
            HAVING COUNT(DISTINCT case_id) > 1
            ORDER BY case_count DESC;
        """,
        "Shared infrastructure across cases": """
            SELECT s.device_id,
                   COUNT(DISTINCT e.case_id) AS case_count,
                   GROUP_CONCAT(DISTINCT e.case_id) AS cases,
                   COUNT(DISTINCT s.account_id) AS account_count
            FROM sessions s
            JOIN events e ON e.session_id = s.session_id
            GROUP BY s.device_id
            HAVING COUNT(DISTINCT e.case_id) > 1
            ORDER BY case_count DESC, account_count DESC;
        """,
        "Repeated target focus": """
            SELECT case_id, target_id,
                   COUNT(DISTINCT account_id) AS accounts,
                   COUNT(*) AS events
            FROM events
            WHERE target_id <> ''
            GROUP BY case_id, target_id
            HAVING COUNT(DISTINCT account_id) >= 3
            ORDER BY accounts DESC, events DESC;
        """,
        "Template reuse across cases": """
            SELECT content_hash,
                   COUNT(DISTINCT case_id) AS case_count,
                   GROUP_CONCAT(DISTINCT case_id) AS cases,
                   COUNT(*) AS content_count
            FROM content
            GROUP BY content_hash
            HAVING COUNT(DISTINCT case_id) > 1
            ORDER BY case_count DESC, content_count DESC
            LIMIT 25;
        """,
        "Critical-case triage metrics": """
            SELECT r.case_id,
                   MIN(CAST(r.triage_minutes AS INTEGER)) AS fastest_triage,
                   ROUND(AVG(CAST(r.triage_minutes AS REAL)),1) AS avg_triage,
                   COUNT(*) AS action_count
            FROM reports_enforcement r
            JOIN cases c ON c.case_id=r.case_id
            WHERE c.severity='Critical'
            GROUP BY r.case_id
            ORDER BY avg_triage;
        """,
    }

    query_name = st.selectbox("Select an investigative question", list(query_options))
    query = query_options[query_name]
    st.code(query.strip(), language="sql")
    st.dataframe(run_query(query), use_container_width=True, hide_index=True)
    st.caption(
        "The SQL result is an investigative lead. It requires contextual review before any conclusion or action."
    )

with tabs[4]:
    st.markdown(
        """
        ## Analytical Method

        The portfolio separates:

        1. **Observed facts** — data directly present in the synthetic records.
        2. **Derived indicators** — counts, scores, links, and temporal features produced through analysis.
        3. **Analytical judgments** — reasoned interpretations of what the evidence may mean.
        4. **Alternative explanations** — benign or competing hypotheses that must be considered.
        5. **Confidence** — the strength and consistency of the supporting evidence.
        6. **Recommended action** — proportionate next steps based on policy and risk.
        7. **Limitations** — missing data, ambiguity, and possible sources of error.

        ## Responsible Automation

        SQL, Python, and Codex-assisted workflows are used to reduce repetitive work, surface patterns,
        and improve reproducibility. Human analysts remain responsible for evidence validation,
        credibility assessment, findings, and recommendations.

        ## Public-Safety Safeguards

        The project uses safe placeholders rather than graphic or operationally useful harmful content.
        All targets and identifiers are fictional. No real platform or user data is included.
        """
    )
