import json
import urllib.error
import urllib.request
import streamlit as st



def get_exchange_rate(base, quote):
    url = f"https://api.frankfurter.dev/v2/rate/{base}/{quote}"
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Streamlit exchange-rate app"
        },
    )

    with urllib.request.urlopen(request, timeout=10) as response:
        return json.loads(response.read().decode("utf-8"))
st.markdown(
    """
    <style>
    .stApp {
        background-color: #E0F7FA;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


st.title("환율 조회 웹앱")

currencies = ["KRW", "USD", "EUR", "JPY", "GBP"]
basic = st.selectbox("기준 통화", currencies)
exchange = st.selectbox("변환할 통화", currencies)
price = st.number_input("금액", min_value=0.0, value=0.0)

if st.button("환율 조회하기"):
    if basic == exchange:
        st.warning("같은 통화끼리는 환율 조회가 필요 없습니다.")
    else:
        try:
            data = get_exchange_rate(basic, exchange)
            converted_price = price * data["rate"]

            st.success(f"1 {basic}= {data['rate']}{exchange}")
            st.write(f"{price}{basic}= {converted_price:.2f}{exchange}")
            st.write("기준일:", data["date"])
        except urllib.error.HTTPError as error:
            error_message = error.read().decode("utf-8")
            st.error(f"환율 정보를 가져오지 못했습니다: {error_message}")
        except Exception as error:
            st.error(f"오류가 발생했습니다: {error}")
