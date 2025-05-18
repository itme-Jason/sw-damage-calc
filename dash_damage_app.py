import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import math

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

app.layout = dbc.Container([
    html.H2("Summoners War Expected Damage Calculator"),
    html.Div("Assumes 100% Crit Rate"),

    dbc.Row([
        dbc.Col([
            html.Label("🔒 Lock to Target Benchmark"),
            dcc.Checklist(id="lock-toggle", options=[{"label": "", "value": "lock"}], value=["lock"], inline=True),
        ], width="auto"),

        dbc.Col([
            html.Label("Target Damage Benchmark"),
            dcc.Slider(id="benchmark", min=1000, max=10000, step=100, value=6000,
                       marks={i: str(i) for i in range(2000, 10001, 1000)})
        ], width=8)
    ], className="my-3"),

    dbc.Row([
        dbc.Col([
            html.Label("Total ATK"),
            dcc.Slider(id="atk", min=2000, max=4000, step=10, value=3000,
                       marks={i: str(i) for i in range(2000, 4001, 200)})
        ]),

        dbc.Col([
            html.Label("Crit Damage (%)"),
            dcc.Slider(id="cd", min=120, max=300, step=5, value=200,
                       marks={i: str(i) for i in range(120, 301, 20)})
        ]),

        dbc.Col([
            html.Label("Number of Fight Sets"),
            dcc.Slider(id="fight_sets", min=0, max=6, step=1, value=0,
                       marks={i: str(i) for i in range(0, 7)})
        ])
    ], className="mb-4"),

    dbc.Row([
        dbc.Col([
            
            html.Div(id="damage-output", className="mt-3")
        ])
    ])
])

@app.callback(
    Output("atk", "value"),
    Output("cd", "value"),
    Output("damage-output", "children"),
    State("lock-toggle", "value"),
    State("atk", "value"),
    State("cd", "value"),
    State("fight_sets", "value"),
    State("benchmark", "value")
)
def update_damage(atk, cd, fight_sets, benchmark, lock):
    atk_bonus = 1 + 0.08 * fight_sets

    if "lock" in lock:
        changed_by = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
        if changed_by == "cd" or changed_by == "fight_sets" or changed_by == "benchmark":
            crit_multiplier = 1 + (cd - 100) / 100
            atk = round(benchmark / (atk_bonus * crit_multiplier))
        elif changed_by == "atk":
            crit_multiplier = benchmark / (atk * atk_bonus)
            cd = round((crit_multiplier - 1) * 100 + 100)
    crit_multiplier = 1 + (cd - 100) / 100

    expected_damage = atk * atk_bonus * crit_multiplier
    pct = expected_damage / benchmark * 100

    if expected_damage >= benchmark:
        result = f"✅ You exceed the {benchmark:,} damage benchmark ({pct:.1f}%) — {expected_damage:,.0f} dmg"
    else:
        result = f"⚠️ You are at {pct:.1f}% of the {benchmark:,} damage benchmark — {expected_damage:,.0f} dmg"

    return atk, cd, result

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8050))
    app.run(host="0.0.0.0", port=port, debug=False)
