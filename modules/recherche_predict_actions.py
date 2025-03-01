import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objs as go
from modules.model import prediction

def afficher_recherche_actions():
    st.markdown("<h1 style='text-align: center; color: #DAA520; font-size:80px'>B&B Finance</h1>", unsafe_allow_html=True)
    st.markdown("<hr style='border:1px solid #444;'>", unsafe_allow_html=True)
    
    st.title("🔎 Recherche et Prévisions d'Actions")
    st.markdown("### Recherchez des actions et visualisez leurs performances ainsi que leurs prévisions.")

    # Barre de recherche pour le symbole de l'action
    symbole = st.text_input("Entrez le symbole de l'action (par exemple, AAPL pour Apple)", "AAPL")

    # Sélection de la période d'historique
    periode = st.selectbox("Sélectionnez la période d'historique", ["1 mois", "3 mois", "6 mois", "1 an", "5 ans", "Max"])

    # Sélection de la période de prédictions
    periode_pred = st.selectbox("Sélectionnez la période à prédire", ["1 mois", "3 mois", "6 mois", "1 an"])
    
    dict_periode_pred = {
        "1 mois": "31",
        "3 mois": "93",
        "6 mois": "186",
        "1 an": "365"
    }
    
    # Correspondance entre la sélection et la période de yfinance
    dict_periode = {
        "1 mois": "1mo",
        "3 mois": "3mo",
        "6 mois": "6mo",
        "1 an": "1y",
        "5 ans": "5y",
        "Max": "max"
    }
    
    predict = st.checkbox('Afficher les prédictions')
    predict

    # Bouton pour lancer la recherche
    if st.button("Rechercher"):
        try:
            with st.spinner('Chargement des données...'):
                # Téléchargement des données
                ticker = yf.Ticker(symbole)
                historique = ticker.history(period=dict_periode[periode])
                
                if historique.empty:
                    st.error("Aucune donnée trouvée pour ce symbole.")
                else:
                    # Affichage des informations de l'action
                    info = ticker.info
                    st.subheader(f"**{info.get('longName', 'Nom non disponible')} ({symbole.upper()})**")
                    st.markdown(f"**Secteur :** {info.get('sector', 'N/A')}")
                    st.markdown(f"**Industrie :** {info.get('industry', 'N/A')}")
                    st.markdown(f"**Site Web :** {info.get('website', 'N/A')}")
                    st.markdown("---")
                    
                    # Récupérer les prédictions
                    if predict:
                        predict_df = prediction(ticker,int(dict_periode_pred[periode_pred]))
                    
                        # Affichage du graphique interactif
                        fig = go.Figure()
                        fig.add_trace(go.Scatter(
                            x=historique.index,
                            y=historique["Close"],
                            mode='lines',
                            name='Prix de clôture'
                        ))
                        fig.add_trace(go.Scatter(
                            x=predict_df['Date'],
                            y=predict_df["Predictions"],
                            mode='lines',
                            name='Prédictions',
                            line=dict(dash='dash')
                        ))
                        fig.update_layout(
                            title=f"Historique du prix de l'action {symbole.upper()}",
                            xaxis_title="Date",
                            yaxis_title="Prix de clôture",
                            template="plotly_dark",
                            paper_bgcolor='#0e1117',
                            plot_bgcolor='#0e1117',
                            font=dict(color='#e6e6e6'),
                            title_font=dict(color='#DAA520')
                        )
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                                                # Affichage du graphique interactif
                        fig = go.Figure()
                        fig.add_trace(go.Scatter(
                            x=historique.index,
                            y=historique["Close"],
                            mode='lines',
                            name='Prix de clôture'
                        ))
                        fig.update_layout(
                            title=f"Historique du prix de l'action {symbole.upper()}",
                            xaxis_title="Date",
                            yaxis_title="Prix de clôture",
                            template="plotly_dark",
                            paper_bgcolor='#0e1117',
                            plot_bgcolor='#0e1117',
                            font=dict(color='#e6e6e6'),
                            title_font=dict(color='#DAA520')
                        )
                        st.plotly_chart(fig, use_container_width=True)

                    # Affichage des indicateurs financiers clés
                    st.markdown("### 📊 Indicateurs Financiers Clés")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Prix actuel", f"${info.get('currentPrice', 'N/A')}")
                        st.metric("Variation sur 1 an", f"{info.get('52WeekChange', 0):.2%}")
                    with col2:
                        st.metric("Capitalisation boursière", f"${info.get('marketCap', 'N/A'):,}")
                        st.metric("PER (TTM)", f"{info.get('trailingPE', 'N/A')}")
                    with col3:
                        st.metric("Bénéfice par action (EPS)", f"${info.get('trailingEps', 'N/A')}")
                        st.metric("Dividende", f"{info.get('dividendYield', 0):.2%}")

                    # Affichage du tableau des données historiques
                    st.markdown("### 🗒️ Données Historiques")
                    st.dataframe(historique[['Open', 'High', 'Low', 'Close', 'Volume']].tail(10))
        except Exception as e:
            st.error(f"Une erreur est survenue : {str(e)}")