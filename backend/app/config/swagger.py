"""
Centralised OpenAPI/Swagger configuration.
"""

tags_metadata = [
    {
        "name": "Health",
        "description": "Endpoints for service‑health monitoring",
    },
]

openapi_kwargs = {
    "openapi_tags": tags_metadata,
    "license_info": {
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
}
