def chunk_faq(faq_list):
    return [
        {"text": f"Câu hỏi: {item['question']}\nTrả lời: {item['answer']}", "metadata": {"type": "faq"}}
        for item in faq_list
    ]


def chunk_policy(policy_list):
    return [
        {
            "text": f"{item['title']}\n{item['content']}",
            "metadata": {"type": "policy", "category": item["category"]}
        }
        for item in policy_list
    ]


def chunk_products(product_list):
    chunks = []
    for product in product_list:
        meta = {
            "type": "product",
            "name": product["name"],
            "url": product["url"],
            "variants": product.get("variants", [])
        }

        variants_text = ""
        if "variants" in product and product["variants"]:
            variants_text = "Các phiên bản:\n"
            for variant in product["variants"]:
                variants_text += f"- Màu {variant.get('color', 'Không rõ')}: {variant.get('price', 'Liên hệ')}\n"

        specs_text = "\n".join([f"{k}: {v}" for k, v in product["specs"].items()])

        chunks.append({
            "text": f"Tên: {product['name']}\nMô tả: {product['description']}\n{variants_text}Thông số kỹ thuật:\n{specs_text}",
            "metadata": meta
        })
    return chunks
