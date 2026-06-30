import json
import time
from typing import Any, Dict, Optional

import httpx
import streamlit as st


DEFAULT_MAIN_API_URL = "http://127.0.0.1:8000"
DEFAULT_MOCK_API_URL = "http://127.0.0.1:8001"


st.set_page_config(
    page_title="AI Support Test Console",
    page_icon="CS",
    layout="wide",
    initial_sidebar_state="expanded",
)


def normalize_base_url(url: str) -> str:
    return url.strip().rstrip("/")


def request_json(
    method: str,
    base_url: str,
    path: str,
    *,
    params: Optional[Dict[str, Any]] = None,
    json_body: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    url = f"{normalize_base_url(base_url)}{path}"
    started = time.perf_counter()
    try:
        with httpx.Client(timeout=20) as client:
            response = client.request(method, url, params=params, json=json_body)
        elapsed_ms = round((time.perf_counter() - started) * 1000)

        try:
            body = response.json()
        except ValueError:
            body = response.text

        return {
            "ok": response.is_success,
            "status_code": response.status_code,
            "elapsed_ms": elapsed_ms,
            "url": str(response.url),
            "body": body,
        }
    except httpx.RequestError as exc:
        elapsed_ms = round((time.perf_counter() - started) * 1000)
        return {
            "ok": False,
            "status_code": None,
            "elapsed_ms": elapsed_ms,
            "url": url,
            "body": {"error": str(exc)},
        }


def show_result(result: Dict[str, Any]) -> None:
    status = result["status_code"] if result["status_code"] is not None else "connection failed"
    if result["ok"]:
        st.success(f"{status} in {result['elapsed_ms']} ms")
    else:
        st.error(f"{status} in {result['elapsed_ms']} ms")
    st.caption(result["url"])
    st.json(result["body"])


def health_badge(label: str, base_url: str, path: str = "/health") -> None:
    result = request_json("GET", base_url, path)
    if result["ok"]:
        st.success(f"{label}: online")
    else:
        st.error(f"{label}: offline")


def compact_product_ids(value: str) -> list[str]:
    return [item.strip() for item in value.split(",") if item.strip()]


if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


st.title("AI Support Test Console")

with st.sidebar:
    st.subheader("Servers")
    main_api_url = st.text_input("Main API URL", DEFAULT_MAIN_API_URL)
    mock_api_url = st.text_input("Mock Backend URL", DEFAULT_MOCK_API_URL)

    col_health_main, col_health_mock = st.columns(2)
    with col_health_main:
        if st.button("Main", use_container_width=True):
            health_badge("Main API", main_api_url)
    with col_health_mock:
        if st.button("Mock", use_container_width=True):
            health_badge("Mock API", mock_api_url, path="/docs")

    st.divider()
    st.subheader("Sample Data")
    st.code(
        "Orders: ORD-1001 / john@example.com\n"
        "Stock: NDX-115, ND-PROP-13-19\n"
        "Search: propeller / northdock\n"
        "Search: oil / marinexparts",
        language="text",
    )


tab_chat, tab_order, tab_stock, tab_search, tab_shipping, tab_case, tab_mock = st.tabs(
    ["Chat", "Order", "Stock", "Search", "Shipping", "Human and Case", "Mock Context"]
)


with tab_chat:
    st.subheader("Chat")
    for item in st.session_state.chat_history:
        with st.chat_message(item["role"]):
            st.write(item["content"])

    with st.form("chat_form"):
        chat_message = st.text_area("Message", "Do you have NDX-115 in stock?")
        chat_email = st.text_input("Email", "john@example.com")
        chat_site = st.selectbox("Site", ["northdock", "marinexparts"])
        submitted = st.form_submit_button("Send Message", use_container_width=True)

    if submitted:
        st.session_state.chat_history.append({"role": "user", "content": chat_message})
        result = request_json(
            "POST",
            main_api_url,
            "/chat/message",
            json_body={"message": chat_message, "email": chat_email, "site": chat_site},
        )
        answer = result["body"].get("answer") if isinstance(result["body"], dict) else None
        if answer:
            st.session_state.chat_history.append({"role": "assistant", "content": answer})
        show_result(result)


with tab_order:
    st.subheader("Order Status")
    col_order_a, col_order_b = st.columns(2)
    with col_order_a:
        order_number = st.text_input("Order Number", "ORD-1001")
    with col_order_b:
        order_email = st.text_input("Customer Email", "john@example.com")

    if st.button("Check Order", use_container_width=True):
        result = request_json(
            "GET",
            main_api_url,
            "/api/order/status",
            params={"order_number": order_number, "email": order_email},
        )
        show_result(result)


with tab_stock:
    st.subheader("Stock")
    sku = st.text_input("SKU", "NDX-115")
    if st.button("Check Stock", use_container_width=True):
        result = request_json(
            "GET",
            main_api_url,
            "/api/product/stock",
            params={"sku": sku},
        )
        show_result(result)


with tab_search:
    st.subheader("Product Search")
    col_search_a, col_search_b = st.columns(2)
    with col_search_a:
        search_query = st.text_input("Query", "propeller")
    with col_search_b:
        search_site = st.selectbox("Search Site", ["northdock", "marinexparts"])

    if st.button("Search Products", use_container_width=True):
        result = request_json(
            "GET",
            main_api_url,
            "/api/product/search",
            params={"query": search_query, "site": search_site},
        )
        show_result(result)


with tab_shipping:
    st.subheader("Shipping Estimate")
    product_ids_text = st.text_input("Product IDs", "prod-001,prod-003")
    col_ship_a, col_ship_b = st.columns(2)
    with col_ship_a:
        postal_code = st.text_input("Postal Code", "2100")
    with col_ship_b:
        country = st.text_input("Country", "DK")

    if st.button("Estimate Shipping", use_container_width=True):
        result = request_json(
            "GET",
            main_api_url,
            "/api/shipping/estimate",
            params={
                "product_ids": compact_product_ids(product_ids_text),
                "postal_code": postal_code,
                "country": country,
            },
        )
        show_result(result)


with tab_case:
    st.subheader("Human Forward")
    with st.form("human_form"):
        human_conversation_id = st.text_input("Conversation ID", "conv_john@example.com")
        human_email = st.text_input("Forward Email", "john@example.com")
        human_question = st.text_area("Question", "Customer needs help with an order.")
        human_attempt = st.text_area("AI Attempt", "I could not verify the order details.")
        forward_submitted = st.form_submit_button("Forward To Human", use_container_width=True)

    if forward_submitted:
        result = request_json(
            "POST",
            main_api_url,
            "/api/human/forward",
            json_body={
                "conversation_id": human_conversation_id,
                "customer_email": human_email,
                "question": human_question,
                "ai_attempt": human_attempt,
            },
        )
        show_result(result)

    st.divider()
    st.subheader("Case Status")
    with st.form("case_form"):
        case_conversation_id = st.text_input("Case Conversation ID", "conv_john@example.com")
        case_status = st.selectbox("Status", ["closed", "reopened"])
        resolution_summary = st.text_area("Resolution Summary", "Resolved by support.")
        case_submitted = st.form_submit_button("Update Case", use_container_width=True)

    if case_submitted:
        result = request_json(
            "POST",
            main_api_url,
            "/api/case/status",
            json_body={
                "conversation_id": case_conversation_id,
                "status": case_status,
                "resolution_summary": resolution_summary,
            },
        )
        show_result(result)


with tab_mock:
    st.subheader("Mock Context")
    col_context_a, col_context_b = st.columns(2)
    with col_context_a:
        context_query = st.text_input("Context Query", "AquaDrive 115 propeller")
    with col_context_b:
        context_email = st.text_input("Context Email", "john@example.com")

    if st.button("Get Context", use_container_width=True):
        result = request_json(
            "GET",
            mock_api_url,
            "/api/context",
            params={"query": context_query, "email": context_email},
        )
        show_result(result)

    st.divider()
    history_email = st.text_input("History Email", "john@example.com")
    history_limit = st.number_input("History Limit", min_value=1, max_value=50, value=10)

    if st.button("Get Conversation History", use_container_width=True):
        result = request_json(
            "GET",
            mock_api_url,
            "/api/conversation/history",
            params={"email": history_email, "limit": int(history_limit)},
        )
        show_result(result)

    with st.expander("Raw Request Templates"):
        st.code(
            json.dumps(
                {
                    "chat": {
                        "method": "POST",
                        "url": f"{normalize_base_url(main_api_url)}/chat/message",
                        "body": {
                            "message": "Do you have NDX-115 in stock?",
                            "email": "john@example.com",
                            "site": "northdock",
                        },
                    },
                    "order": {
                        "method": "GET",
                        "url": f"{normalize_base_url(main_api_url)}/api/order/status?order_number=ORD-1001&email=john@example.com",
                    },
                },
                indent=2,
            ),
            language="json",
        )
