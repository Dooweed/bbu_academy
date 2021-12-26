def get_model(purchase_id: str):
    if "S" in purchase_id:
        from small_purchase.models import SmallPurchaseRecord
        queryset = SmallPurchaseRecord.objects.filter(id=int(purchase_id.replace("S", "")))
    else:
        from purchase.models import PurchaseRecord
        queryset = PurchaseRecord.objects.filter(id=int(purchase_id))
    if queryset.exists():
        return queryset.first()
    else:
        return None
