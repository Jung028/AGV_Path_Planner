from fastapi import FastAPI, Query
from pydantic import BaseModel
import logging
from typing import List, Optional, Dict

# Initialize FastAPI app
app = FastAPI()

# Setup logging
logging.basicConfig(filename="api_requests.log", level=logging.INFO, format="%(asctime)s - %(message)s")

# ========================= SKU SYNC =========================
class Packing(BaseModel):
    sku_packing_spec: str
    primary: Dict[str, float]
    secondary: Optional[Dict[str, float]] = None
    tertiary: Optional[Dict[str, float]] = None

class SKU(BaseModel):
    owner_code: str
    sku_id: str
    sku_code: str
    sku_name: str
    sku_price: float
    unit: str
    remark: str
    dimensions: Dict[str, float]
    weight: Dict[str, float]
    stock_limits: Dict[str, int]
    sku_shelf_life: int
    sku_specification: str
    sku_status: int
    sku_abc: str
    is_sequence_sku: int
    sku_production_location: str
    sku_brand: str
    sku_attributes: Dict[str, str]
    sku_pic_url: str
    is_bar_code_full_update: int
    sku_bar_code_list: List[Dict[str, str]]
    sku_packing: List[Packing]

class SKUSyncRequest(BaseModel):
    header: Dict[str, str]
    body: Dict[str, List[SKU]]

@app.post("/api/inventory/sync")
async def sku_sync(request: SKUSyncRequest, warehouse: str = Query(...), owner: str = Query(...)):
    """Handles SKU Synchronization"""
    
    logging.info(f"SKU Sync Request: Warehouse: {warehouse}, Owner: {owner}, Data: {request.dict()}")
    print(f"Received SKU Sync Request: {request.dict()}")

    return {
        "message": "SKU Synchronization Successful",
        "warehouse": warehouse,
        "owner": owner,
        "sku_count": len(request.body["sku_list"]),
    }

# ========================= PUTAWAY ORDER CREATION =========================
class SKUDetail(BaseModel):
    sku_code: str
    sku_level: int
    owner_code: str
    sku_amount: int
    sku_out_batch_code: Optional[str] = None
    sku_production_date: Optional[int] = None
    sku_expiration_date: Optional[int] = None

class ReceiptInfo(BaseModel):
    receipt_code: str
    receipt_type: int
    pallet_code: str
    creation_date: int
    supplier_code: str
    carrier_code: str
    remark: str

class Receipt(BaseModel):
    receipt_info: ReceiptInfo
    sku_details: List[SKUDetail]

class PutawayRequest(BaseModel):
    header: Dict[str, str]
    body: Dict[str, List[Receipt]]

@app.post("/api/putaway/create")
async def putaway_order(request: PutawayRequest, warehouse: str = Query(...), owner: str = Query(...)):
    """Handles Putaway Order Creation"""
    
    logging.info(f"Putaway Order Request: Warehouse: {warehouse}, Owner: {owner}, Data: {request.dict()}")
    print(f"Received Putaway Order Request: {request.dict()}")

    return {
        "message": "Putaway Order Created Successfully",
        "warehouse": warehouse,
        "owner": owner,
        "receipt_count": len(request.body["receipts"]),
    }

# ========================= PUTAWAY ORDER CONFIRMATION =========================
class ConfirmSKUDetail(BaseModel):
    sku_code: str
    owner_code: str
    sku_level: int
    sku_receipt_flag: int
    sku_amount: int

class ConfirmReceiptInfo(BaseModel):
    receipt_code: str
    pallet_code: str
    receipt_type: int
    receipt_status: int
    status: int
    completion_time: int

class ConfirmReceipt(BaseModel):
    receipt_info: ConfirmReceiptInfo
    sku_details: List[ConfirmSKUDetail]

class PutawayConfirmRequest(BaseModel):
    header: Dict[str, str]
    body: Dict[str, List[ConfirmReceipt]]

@app.post("/api/putaway/confirm")
async def putaway_confirm(request: PutawayConfirmRequest, warehouse: str = Query(...), owner: str = Query(...)):
    """Handles Putaway Order Confirmation"""
    
    logging.info(f"Putaway Confirm Request: Warehouse: {warehouse}, Owner: {owner}, Data: {request.dict()}")
    print(f"Received Putaway Confirm Request: {request.dict()}")

    return {
        "message": "Putaway Order Confirmed Successfully",
        "warehouse": warehouse,
        "owner": owner,
        "receipt_count": len(request.body["receipts"]),
    }


# ========================= PUTAWAY ORDER CANCELLATION =========================
class CancelReceiptInfo(BaseModel):
    warehouse_code: str
    receipt_code: str
    owner_code: str
    cancel_date: int
    remark: Optional[str] = ""

class CancelReceipt(BaseModel):
    receipt_info: CancelReceiptInfo

class PutawayCancelRequest(BaseModel):
    header: Dict[str, str]
    body: Dict[str, List[CancelReceipt]]

@app.post("/api/putaway/cancel")
async def putaway_cancel(request: PutawayCancelRequest, warehouse: str = Query(...), owner: str = Query(...)):
    """Handles Putaway Order Cancellation"""
    
    logging.info(f"Putaway Cancel Request: Warehouse: {warehouse}, Owner: {owner}, Data: {request.dict()}")
    print(f"Received Putaway Cancel Request: {request.dict()}")

    return {
        "message": "Putaway Order Canceled Successfully",
        "warehouse": warehouse,
        "owner": owner,
        "receipt_count": len(request.body["receipts"]),
    }



# ========================= PICK ORDER CREATION =========================
class PrintDetails(BaseModel):
    type: int
    content: str

class CarrierDetails(BaseModel):
    type: int
    code: str
    name: str
    waybill_code: str

class OrderDates(BaseModel):
    creation_date: int
    expected_finish_date: int

class OrderDetails(BaseModel):
    out_order_code: str
    order_type: int
    out_wave_code: str
    owner_code: str
    is_allow_pick_lack: int
    print: PrintDetails
    carrier: CarrierDetails
    is_allow_lack: int
    dates: OrderDates
    priority: int

class SkuItem(BaseModel):
    sku_code: str
    sku_id: str
    out_batch_code: Optional[str] = None
    sku_level: int
    amount: int
    production_date: Optional[int] = None
    expiration_date: Optional[int] = None

class Order(BaseModel):
    order_details: OrderDetails
    sku_items: List[SkuItem]

class PickOrderRequest(BaseModel):
    header: Dict[str, str]
    body: Dict[str, List[Order]]

@app.post("/api/pick/create")
async def pick_order_create(request: PickOrderRequest, warehouse: str = Query(...), owner: str = Query(...)):
    """Handles Pick Order Creation"""

    logging.info(f"Pick Order Request: Warehouse: {warehouse}, Owner: {owner}, Data: {request.dict()}")
    print(f"Received Pick Order Request: {request.dict()}")

    return {
        "message": "Pick Order Created Successfully",
        "warehouse": warehouse,
        "owner": owner,
        "order_count": len(request.body["orders"]),
    }


# ========================= PICK ORDER CONFIRMATION =========================
class OrderDates(BaseModel):
    production_date: int
    expiration_date: int

class SerialNumber(BaseModel):
    sequence_no: str

class SkuItem(BaseModel):
    item: int
    sku_code: str
    bar_code: Optional[str] = None
    sku_level: int
    plan_amount: int
    pickup_amount: int
    out_batch_code: Optional[str] = None
    dates: OrderDates
    remark: Optional[str] = None
    owner_code: str
    sn_list: Optional[List[SerialNumber]] = None

class ContainerSkuItem(BaseModel):
    item: int
    sku_code: str
    bar_code: Optional[str] = None
    sku_level: int
    amount: int
    out_batch_code: Optional[str] = None
    dates: OrderDates
    owner_code: str
    sn_list: Optional[List[SerialNumber]] = None

class ContainerDetails(BaseModel):
    picker: str
    container_code: str
    sku_amount: int
    sku_type_amount: int
    creation_date: int
    sku_items: List[ContainerSkuItem]

class OrderDetails(BaseModel):
    out_order_code: str
    status: int
    warehouse_code: str
    owner_code: str
    is_exception: int
    order_type: int
    plan_sku_amount: int
    pickup_sku_amount: int
    pick_type: int
    lack_flag: int
    container_amount: int
    finish_date: int

class Order(BaseModel):
    order_details: OrderDetails
    sku_items: List[SkuItem]
    containers: List[ContainerDetails]

class PickOrderConfirmRequest(BaseModel):
    header: Dict[str, str]
    body: Dict[str, List[Order]]

@app.post("/api/pick/confirm")
async def pick_order_confirm(request: PickOrderConfirmRequest, warehouse: str = Query(...), owner: str = Query(...)):
    """Handles Pick Order Confirmation"""

    logging.info(f"Pick Order Confirmation Request: Warehouse: {warehouse}, Owner: {owner}, Data: {request.dict()}")
    print(f"Received Pick Order Confirmation Request: {request.dict()}")

    return {
        "message": "Pick Order Confirmed Successfully",
        "warehouse": warehouse,
        "owner": owner,
        "order_count": len(request.body["orders"]),
    }

