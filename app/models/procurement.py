"""
采购管理模型
"""
from sqlalchemy import Column, String, Text, Boolean, Integer, Float, DateTime, JSON, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import enum

from .base import Base


class ProcurementStatus(str, enum.Enum):
    """采购需求状态枚举"""
    DRAFT = "draft"  # 草稿
    SUBMITTED = "submitted"  # 已提交
    UNDER_REVIEW = "under_review"  # 审核中
    APPROVED = "approved"  # 已批准
    REJECTED = "rejected"  # 已拒绝
    CANCELLED = "cancelled"  # 已取消


class OrderStatus(str, enum.Enum):
    """采购订单状态枚举"""
    DRAFT = "draft"  # 草稿
    PENDING_APPROVAL = "pending_approval"  # 待审批
    APPROVED = "approved"  # 已批准
    REJECTED = "rejected"  # 已拒绝
    ISSUED = "issued"  # 已发出
    CONFIRMED = "confirmed"  # 供应商已确认
    PARTIALLY_DELIVERED = "partially_delivered"  # 部分交货
    DELIVERED = "delivered"  # 已交货
    PARTIALLY_RECEIVED = "partially_received"  # 部分收货
    RECEIVED = "received"  # 已收货
    INVOICED = "invoiced"  # 已开票
    PAID = "paid"  # 已付款
    CLOSED = "closed"  # 已关闭
    CANCELLED = "cancelled"  # 已取消


class DeliveryStatus(str, enum.Enum):
    """送货单状态枚举"""
    PENDING = "pending"  # 待发货
    IN_TRANSIT = "in_transit"  # 运输中
    DELIVERED = "delivered"  # 已送达
    RECEIVED = "received"  # 已收货
    CANCELLED = "cancelled"  # 已取消


class ReceiptStatus(str, enum.Enum):
    """入库单状态枚举"""
    PENDING = "pending"  # 待验收
    INSPECTING = "inspecting"  # 验收中
    ACCEPTED = "accepted"  # 已验收
    PARTIALLY_ACCEPTED = "partially_accepted"  # 部分验收
    REJECTED = "rejected"  # 已拒收
    STORED = "stored"  # 已入库
    CANCELLED = "cancelled"  # 已取消


class ProcurementRequest(Base):
    """采购需求模型"""
    __tablename__ = 'procurement_request'

    # 需求信息
    request_number = Column(
        String(50),
        unique=True,
        nullable=False,
        index=True,
        comment='需求编号'
    )
    title = Column(
        String(200),
        nullable=False,
        comment='需求标题'
    )
    description = Column(
        Text,
        nullable=True,
        comment='需求描述'
    )
    department = Column(
        String(100),
        nullable=False,
        comment='申请部门'
    )
    purpose = Column(
        Text,
        nullable=True,
        comment='用途说明'
    )
    priority = Column(
        String(20),
        nullable=False,
        default='normal',
        comment='优先级（urgent:紧急, high:高, normal:正常, low:低）'
    )
    required_date = Column(
        DateTime,
        nullable=True,
        comment='要求到货日期'
    )
    budget_amount = Column(
        Float,
        nullable=True,
        comment='预算金额'
    )
    budget_code = Column(
        String(100),
        nullable=True,
        comment='预算编码'
    )

    # 状态
    status = Column(
        Enum(ProcurementStatus),
        nullable=False,
        default=ProcurementStatus.DRAFT,
        index=True,
        comment='需求状态'
    )
    submission_date = Column(
        DateTime,
        nullable=True,
        comment='提交日期'
    )
    approval_date = Column(
        DateTime,
        nullable=True,
        comment='审批日期'
    )

    # 审批信息
    approver_id = Column(
        UUID(as_uuid=True),
        ForeignKey('user.id'),
        nullable=True,
        comment='审批人ID'
    )
    approval_notes = Column(
        Text,
        nullable=True,
        comment='审批意见'
    )
    approval_flow = Column(
        JSON,
        nullable=True,
        comment='审批流程记录'
    )

    # 关联信息
    requester_id = Column(
        UUID(as_uuid=True),
        ForeignKey('user.id'),
        nullable=False,
        index=True,
        comment='申请人ID'
    )
    related_project = Column(
        String(200),
        nullable=True,
        comment='关联项目'
    )
    tags = Column(
        JSON,
        nullable=True,
        comment='标签'
    )
    attachments = Column(
        JSON,
        nullable=True,
        comment='附件'
    )

    # 关系
    requester = relationship(
        'User',
        back_populates='procurement_requests',
        lazy='selectin',
        foreign_keys=[requester_id]
    )
    approver = relationship(
        'User',
        back_populates='approved_requests',
        lazy='selectin',
        foreign_keys=[approver_id]
    )
    items = relationship(
        'RequestItem',
        back_populates='request',
        lazy='selectin',
        cascade='all, delete-orphan'
    )
    purchase_orders = relationship(
        'PurchaseOrder',
        back_populates='procurement_request',
        lazy='dynamic',
        cascade='all, delete-orphan'
    )

    def __repr__(self) -> str:
        return f'<ProcurementRequest {self.request_number}>'


class RequestItem(Base):
    """采购需求项模型"""
    __tablename__ = 'request_item'

    request_id = Column(
        UUID(as_uuid=True),
        ForeignKey('procurement_request.id', ondelete='CASCADE'),
        nullable=False,
        index=True,
        comment='需求ID'
    )
    item_name = Column(
        String(200),
        nullable=False,
        comment='物品名称'
    )
    item_code = Column(
        String(100),
        nullable=True,
        comment='物品编码'
    )
    specification = Column(
        Text,
        nullable=True,
        comment='规格型号'
    )
    unit = Column(
        String(50),
        nullable=True,
        comment='单位'
    )
    quantity = Column(
        Float,
        nullable=False,
        comment='数量'
    )
    estimated_unit_price = Column(
        Float,
        nullable=True,
        comment='预估单价'
    )
    estimated_total_price = Column(
        Float,
        nullable=True,
        comment='预估总价'
    )
    brand = Column(
        String(100),
        nullable=True,
        comment='品牌'
    )
    manufacturer = Column(
        String(200),
        nullable=True,
        comment='生产厂家'
    )
    required_date = Column(
        DateTime,
        nullable=True,
        comment='要求到货日期'
    )
    usage_location = Column(
        String(200),
        nullable=True,
        comment='使用地点'
    )
    technical_requirements = Column(
        Text,
        nullable=True,
        comment='技术要求'
    )
    remarks = Column(
        Text,
        nullable=True,
        comment='备注'
    )

    # 关系
    request = relationship(
        'ProcurementRequest',
        back_populates='items',
        lazy='selectin'
    )

    def __repr__(self) -> str:
        return f'<RequestItem {self.item_name} x{self.quantity}>'


class PurchaseOrder(Base):
    """采购订单模型"""
    __tablename__ = 'purchase_order'

    # 订单信息
    order_number = Column(
        String(50),
        unique=True,
        nullable=False,
        index=True,
        comment='订单编号'
    )
    title = Column(
        String(200),
        nullable=False,
        comment='订单标题'
    )
    status = Column(
        Enum(OrderStatus),
        nullable=False,
        default=OrderStatus.DRAFT,
        index=True,
        comment='订单状态'
    )

    # 关联信息
    procurement_request_id = Column(
        UUID(as_uuid=True),
        ForeignKey('procurement_request.id'),
        nullable=True,
        index=True,
        comment='采购需求ID'
    )
    supplier_id = Column(
        UUID(as_uuid=True),
        ForeignKey('supplier.id'),
        nullable=False,
        index=True,
        comment='供应商ID'
    )

    # 合同信息
    contract_number = Column(
        String(100),
        nullable=True,
        comment='合同编号'
    )
    contract_date = Column(
        DateTime,
        nullable=True,
        comment='合同日期'
    )
    contract_amount = Column(
        Float,
        nullable=False,
        comment='合同金额'
    )
    currency = Column(
        String(10),
        nullable=False,
        default='CNY',
        comment='货币'
    )
    payment_terms = Column(
        Text,
        nullable=True,
        comment='付款条件'
    )
    delivery_terms = Column(
        Text,
        nullable=True,
        comment='交货条件'
    )
    warranty_terms = Column(
        Text,
        nullable=True,
        comment='质保条款'
    )

    # 时间信息
    order_date = Column(
        DateTime,
        nullable=False,
        comment='订单日期'
    )
    expected_delivery_date = Column(
        DateTime,
        nullable=True,
        comment='预计交货日期'
    )
    actual_delivery_date = Column(
        DateTime,
        nullable=True,
        comment='实际交货日期'
    )
    completion_date = Column(
        DateTime,
        nullable=True,
        comment='完成日期'
    )

    # 财务信息
    tax_rate = Column(
        Float,
        default=0.0,
        nullable=False,
        comment='税率'
    )
    tax_amount = Column(
        Float,
        default=0.0,
        nullable=False,
        comment='税额'
    )
    total_amount = Column(
        Float,
        nullable=False,
        comment='总金额'
    )
    advance_payment_amount = Column(
        Float,
        default=0.0,
        nullable=False,
        comment='预付款金额'
    )
    advance_payment_percentage = Column(
        Float,
        default=0.0,
        nullable=False,
        comment='预付款比例'
    )

    # 审批信息
    approver_id = Column(
        UUID(as_uuid=True),
        ForeignKey('user.id'),
        nullable=True,
        comment='审批人ID'
    )
    approval_date = Column(
        DateTime,
        nullable=True,
        comment='审批日期'
    )
    approval_notes = Column(
        Text,
        nullable=True,
        comment='审批意见'
    )

    # 备注
    remarks = Column(
        Text,
        nullable=True,
        comment='备注'
    )
    attachments = Column(
        JSON,
        nullable=True,
        comment='附件'
    )

    # 关系
    supplier = relationship(
        'Supplier',
        back_populates='purchase_orders',
        lazy='selectin'
    )
    procurement_request = relationship(
        'ProcurementRequest',
        back_populates='purchase_orders',
        lazy='selectin'
    )
    items = relationship(
        'OrderItem',
        back_populates='order',
        lazy='selectin',
        cascade='all, delete-orphan'
    )
    delivery_notes = relationship(
        'DeliveryNote',
        back_populates='purchase_order',
        lazy='dynamic',
        cascade='all, delete-orphan'
    )
    inventory_receipts = relationship(
        'InventoryReceipt',
        back_populates='purchase_order',
        lazy='dynamic',
        cascade='all, delete-orphan'
    )

    def __repr__(self) -> str:
        return f'<PurchaseOrder {self.order_number}>'


class OrderItem(Base):
    """采购订单项模型"""
    __tablename__ = 'order_item'

    order_id = Column(
        UUID(as_uuid=True),
        ForeignKey('purchase_order.id', ondelete='CASCADE'),
        nullable=False,
        index=True,
        comment='订单ID'
    )
    item_name = Column(
        String(200),
        nullable=False,
        comment='物品名称'
    )
    item_code = Column(
        String(100),
        nullable=True,
        comment='物品编码'
    )
    specification = Column(
        Text,
        nullable=True,
        comment='规格型号'
    )
    unit = Column(
        String(50),
        nullable=True,
        comment='单位'
    )
    quantity = Column(
        Float,
        nullable=False,
        comment='数量'
    )
    unit_price = Column(
        Float,
        nullable=False,
        comment='单价'
    )
    total_price = Column(
        Float,
        nullable=False,
        comment='总价'
    )
    currency = Column(
        String(10),
        nullable=False,
        default='CNY',
        comment='货币'
    )
    brand = Column(
        String(100),
        nullable=True,
        comment='品牌'
    )
    manufacturer = Column(
        String(200),
        nullable=True,
        comment='生产厂家'
    )
    delivery_date = Column(
        DateTime,
        nullable=True,
        comment='要求交货日期'
    )
    warranty_period = Column(
        String(100),
        nullable=True,
        comment='质保期'
    )
    technical_requirements = Column(
        Text,
        nullable=True,
        comment='技术要求'
    )
    remarks = Column(
        Text,
        nullable=True,
        comment='备注'
    )

    # 关系
    order = relationship(
        'PurchaseOrder',
        back_populates='items',
        lazy='selectin'
    )

    def __repr__(self) -> str:
        return f'<OrderItem {self.item_name} x{self.quantity}>'


class DeliveryNote(Base):
    """送货单模型"""
    __tablename__ = 'delivery_note'

    # 送货单信息
    delivery_number = Column(
        String(50),
        unique=True,
        nullable=False,
        index=True,
        comment='送货单号'
    )
    status = Column(
        Enum(DeliveryStatus),
        nullable=False,
        default=DeliveryStatus.PENDING,
        index=True,
        comment='送货状态'
    )

    # 关联信息
    purchase_order_id = Column(
        UUID(as_uuid=True),
        ForeignKey('purchase_order.id'),
        nullable=False,
        index=True,
        comment='采购订单ID'
    )
    supplier_id = Column(
        UUID(as_uuid=True),
        ForeignKey('supplier.id'),
        nullable=False,
        comment='供应商ID'
    )

    # 物流信息
    logistics_company = Column(
        String(100),
        nullable=True,
        comment='物流公司'
    )
    tracking_number = Column(
        String(100),
        nullable=True,
        comment='运单号'
    )
    delivery_date = Column(
        DateTime,
        nullable=True,
        comment='发货日期'
    )
    expected_arrival_date = Column(
        DateTime,
        nullable=True,
        comment='预计到达日期'
    )
    actual_arrival_date = Column(
        DateTime,
        nullable=True,
        comment='实际到达日期'
    )

    # 收货信息
    receiver_id = Column(
        UUID(as_uuid=True),
        ForeignKey('user.id'),
        nullable=True,
        comment='收货人ID'
    )
    receipt_date = Column(
        DateTime,
        nullable=True,
        comment='收货日期'
    )
    receipt_notes = Column(
        Text,
        nullable=True,
        comment='收货备注'
    )

    # 备注
    remarks = Column(
        Text,
        nullable=True,
        comment='备注'
    )
    attachments = Column(
        JSON,
        nullable=True,
        comment='附件'
    )

    # 关系
    purchase_order = relationship(
        'PurchaseOrder',
        back_populates='delivery_notes',
        lazy='selectin'
    )
    supplier = relationship(
        'Supplier',
        lazy='selectin'
    )
    receiver = relationship(
        'User',
        lazy='selectin'
    )
    items = relationship(
        'DeliveryItem',
        back_populates='delivery_note',
        lazy='selectin',
        cascade='all, delete-orphan'
    )

    def __repr__(self) -> str:
        return f'<DeliveryNote {self.delivery_number}>'


class DeliveryItem(Base):
    """送货单项模型"""
    __tablename__ = 'delivery_item'

    delivery_note_id = Column(
        UUID(as_uuid=True),
        ForeignKey('delivery_note.id', ondelete='CASCADE'),
        nullable=False,
        index=True,
        comment='送货单ID'
    )
    order_item_id = Column(
        UUID(as_uuid=True),
        ForeignKey('order_item.id'),
        nullable=True,
        comment='订单项ID'
    )
    item_name = Column(
        String(200),
        nullable=False,
        comment='物品名称'
    )
    item_code = Column(
        String(100),
        nullable=True,
        comment='物品编码'
    )
    specification = Column(
        Text,
        nullable=True,
        comment='规格型号'
    )
    unit = Column(
        String(50),
        nullable=True,
        comment='单位'
    )
    ordered_quantity = Column(
        Float,
        nullable=False,
        comment='订购数量'
    )
    delivered_quantity = Column(
        Float,
        nullable=False,
        comment='送货数量'
    )
    unit_price = Column(
        Float,
        nullable=True,
        comment='单价'
    )
    total_price = Column(
        Float,
        nullable=True,
        comment='总价'
    )
    batch_number = Column(
        String(100),
        nullable=True,
        comment='批号'
    )
    production_date = Column(
        DateTime,
        nullable=True,
        comment='生产日期'
    )
    expiry_date = Column(
        DateTime,
        nullable=True,
        comment='有效期至'
    )
    quality_status = Column(
        String(50),
        nullable=True,
        comment='质量状态'
    )
    remarks = Column(
        Text,
        nullable=True,
        comment='备注'
    )

    # 关系
    delivery_note = relationship(
        'DeliveryNote',
        back_populates='items',
        lazy='selectin'
    )
    order_item = relationship(
        'OrderItem',
        lazy='selectin'
    )

    def __repr__(self) -> str:
        return f'<DeliveryItem {self.item_name} x{self.delivered_quantity}>'


class InventoryReceipt(Base):
    """入库单模型"""
    __tablename__ = 'inventory_receipt'

    # 入库单信息
    receipt_number = Column(
        String(50),
        unique=True,
        nullable=False,
        index=True,
        comment='入库单号'
    )
    status = Column(
        Enum(ReceiptStatus),
        nullable=False,
        default=ReceiptStatus.PENDING,
        index=True,
        comment='入库状态'
    )

    # 关联信息
    purchase_order_id = Column(
        UUID(as_uuid=True),
        ForeignKey('purchase_order.id'),
        nullable=False,
        index=True,
        comment='采购订单ID'
    )
    delivery_note_id = Column(
        UUID(as_uuid=True),
        ForeignKey('delivery_note.id'),
        nullable=True,
        comment='送货单ID'
    )

    # 验收信息
    inspector_id = Column(
        UUID(as_uuid=True),
        ForeignKey('user.id'),
        nullable=True,
        comment='验收人ID'
    )
    inspection_date = Column(
        DateTime,
        nullable=True,
        comment='验收日期'
    )
    inspection_method = Column(
        String(100),
        nullable=True,
        comment='验收方式'
    )
    inspection_result = Column(
        Text,
        nullable=True,
        comment='验收结果'
    )
    quality_rating = Column(
        String(50),
        nullable=True,
        comment='质量评级'
    )

    # 入库信息
    warehouse_location = Column(
        String(200),
        nullable=True,
        comment='仓库位置'
    )
    storage_condition = Column(
        String(100),
        nullable=True,
        comment='存储条件'
    )
    receipt_date = Column(
        DateTime,
        nullable=True,
        comment='入库日期'
    )
    storekeeper_id = Column(
        UUID(as_uuid=True),
        ForeignKey('user.id'),
        nullable=True,
        comment='仓管员ID'
    )

    # 备注
    remarks = Column(
        Text,
        nullable=True,
        comment='备注'
    )
    attachments = Column(
        JSON,
        nullable=True,
        comment='附件'
    )

    # 关系
    purchase_order = relationship(
        'PurchaseOrder',
        back_populates='inventory_receipts',
        lazy='selectin'
    )
    delivery_note = relationship(
        'DeliveryNote',
        lazy='selectin'
    )
    inspector = relationship(
        'User',
        foreign_keys=[inspector_id],
        lazy='selectin'
    )
    storekeeper = relationship(
        'User',
        foreign_keys=[storekeeper_id],
        lazy='selectin'
    )
    items = relationship(
        'ReceiptItem',
        back_populates='inventory_receipt',
        lazy='selectin',
        cascade='all, delete-orphan'
    )

    def __repr__(self) -> str:
        return f'<InventoryReceipt {self.receipt_number}>'


class ReceiptItem(Base):
    """入库单项模型"""
    __tablename__ = 'receipt_item'

    receipt_id = Column(
        UUID(as_uuid=True),
        ForeignKey('inventory_receipt.id', ondelete='CASCADE'),
        nullable=False,
        index=True,
        comment='入库单ID'
    )
    delivery_item_id = Column(
        UUID(as_uuid=True),
        ForeignKey('delivery_item.id'),
        nullable=True,
        comment='送货单项ID'
    )
    item_name = Column(
        String(200),
        nullable=False,
        comment='物品名称'
    )
    item_code = Column(
        String(100),
        nullable=True,
        comment='物品编码'
    )
    specification = Column(
        Text,
        nullable=True,
        comment='规格型号'
    )
    unit = Column(
        String(50),
        nullable=True,
        comment='单位'
    )
    delivered_quantity = Column(
        Float,
        nullable=False,
        comment='送货数量'
    )
    accepted_quantity = Column(
        Float,
        nullable=False,
        comment='验收数量'
    )
    rejected_quantity = Column(
        Float,
        default=0.0,
        nullable=False,
        comment='拒收数量'
    )
    unit_price = Column(
        Float,
        nullable=True,
        comment='单价'
    )
    total_price = Column(
        Float,
        nullable=True,
        comment='总价'
    )
    batch_number = Column(
        String(100),
        nullable=True,
        comment='批号'
    )
    production_date = Column(
        DateTime,
        nullable=True,
        comment='生产日期'
    )
    expiry_date = Column(
        DateTime,
        nullable=True,
        comment='有效期至'
    )
    storage_location = Column(
        String(200),
        nullable=True,
        comment='存储位置'
    )
    quality_status = Column(
        String(50),
        nullable=True,
        comment='质量状态'
    )
    rejection_reason = Column(
        Text,
        nullable=True,
        comment='拒收原因'
    )
    remarks = Column(
        Text,
        nullable=True,
        comment='备注'
    )

    # 关系
    inventory_receipt = relationship(
        'InventoryReceipt',
        back_populates='items',
        lazy='selectin'
    )
    delivery_item = relationship(
        'DeliveryItem',
        lazy='selectin'
    )

    def __repr__(self) -> str:
        return f'<ReceiptItem {self.item_name} x{self.accepted_quantity}>'