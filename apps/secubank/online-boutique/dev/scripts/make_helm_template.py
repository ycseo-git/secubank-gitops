import yaml
from pathlib import Path

src = Path("/home/ycseo/secubank-pipeline/online-boutique/release/kubernetes-manifests.yaml")
dst = Path("/home/ycseo/secubank-pipeline/gitops-repo/apps/secubank/online-boutique/dev/chart/templates/online-boutique.yaml")

image_keys = {
    "frontend": "frontend",
    "cartservice": "cartservice",
    "checkoutservice": "checkoutservice",
    "currencyservice": "currencyservice",
    "emailservice": "emailservice",
    "paymentservice": "paymentservice",
    "productcatalogservice": "productcatalogservice",
    "recommendationservice": "recommendationservice",
    "shippingservice": "shippingservice",
    "adservice": "adservice",
}

docs = list(yaml.safe_load_all(src.read_text()))

for doc in docs:
    if not isinstance(doc, dict):
        continue

    kind = doc.get("kind")
    meta = doc.get("metadata", {})
    name = meta.get("name")

    if kind in ["Deployment", "Service", "ServiceAccount", "ConfigMap"]:
        meta.pop("namespace", None)

    if kind == "Deployment" and name in image_keys:
        key = image_keys[name]
        containers = doc["spec"]["template"]["spec"].get("containers", [])
        for c in containers:
            c["image"] = f"{{{{ .Values.images.{key}.repository }}}}:{{{{ .Values.images.{key}.tag }}}}"

out = ""
for doc in docs:
    if doc:
        out += "---\n"
        out += yaml.safe_dump(doc, sort_keys=False)

dst.write_text(out)
print(f"written: {dst}")
