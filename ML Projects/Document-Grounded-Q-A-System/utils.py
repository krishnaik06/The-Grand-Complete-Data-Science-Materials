


def format_sources(source_documents):
    formatted_sources = []

    seen = set()  # to avoid duplicates

    for doc in source_documents:
        meta = doc.metadata

        source_name = meta.get("source", "Unknown source")
        page = meta.get("page", None)
        total_pages = meta.get("total_pages", None)

        key = (source_name, page)
        if key in seen:
            continue
        seen.add(key)

        entry = {
            "source": source_name,
            "page": page + 1 if page is not None else None,
            "total_pages": total_pages,
            "excerpt": doc.page_content[:300] + "..."
        }

        formatted_sources.append(entry)

    return formatted_sources
