"""
供应商模型
"""
from sqlalchemy import Column, String, Text, Boolean, Integer, Float, DateTime, JSON, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from .base import Base


class Supplier(Base):
    """供应商模型"""
    __tablename__ = 'supplier'

    # 基本信息
    name = Column(
        String(200),
        nullable=False,
        index=True,
        comment='供应商名称'
    )
    code = Column(
        String(50),
        unique=True,
        nullable=False,
        index=True,
        comment='供应商编码'
    )
    type = Column(
        String(50),
        nullable=False,
        default='general',
        comment='供应商类型（general:普通, strategic:战略, key:关键）'
    )
    status = Column(
        String(20),
        nullable=False,
        default='active',
        index=True,
        comment='状态（active:活跃, inactive:不活跃, suspended:暂停, blacklisted:黑名单）'
    )

    # 联系信息
    contact_person = Column(
        String(100),
        nullable=True,
        comment='联系人'
    )
    contact_phone = Column(
        String(20),
        nullable=True,
        comment='联系电话'
    )
    contact_email = Column(
        String(255),
        nullable=True,
        comment='联系邮箱'
    )
    contact_address = Column(
        Text,
        nullable=True,
        comment='联系地址'
    )

    # 公司信息
    company_name = Column(
        String(200),
        nullable=True,
        comment='公司名称'
    )
    registration_number = Column(
        String(100),
        nullable=True,
        unique=True,
        comment='工商注册号'
    )
    tax_number = Column(
        String(100),
        nullable=True,
        comment='税务登记号'
    )
    business_scope = Column(
        Text,
        nullable=True,
        comment='经营范围'
    )
    registered_capital = Column(
        Float,
        nullable=True,
        comment='注册资本（万元）'
    )
    established_date = Column(
        DateTime,
        nullable=True,
        comment='成立日期'
    )

    # 资质信息
    qualification_level = Column(
        String(50),
        nullable=True,
        comment='资质等级'
    )
    qualification_certificates = Column(
        JSON,
        nullable=True,
        comment='资质证书信息'
    )
    quality_system = Column(
        String(100),
        nullable=True,
        comment='质量体系认证'
    )
    industry_certifications = Column(
        JSON,
        nullable=True,
        comment='行业认证'
    )

    # 评估信息
    overall_rating = Column(
        Float,
        default=0.0,
        nullable=False,
        comment='综合评分（0-5）'
    )
    quality_rating = Column(
        Float,
        default=0.0,
        nullable=False,
        comment='质量评分'
    )
    delivery_rating = Column(
        Float,
        default=0.0,
        nullable=False,
        comment='交付评分'
    )
    service_rating = Column(
        Float,
        default=0.0,
        nullable=False,
        comment='服务评分'
    )
    price_rating = Column(
        Float,
        default=0.0,
        nullable=False,
        comment='价格评分'
    )
    assessment_date = Column(
        DateTime,
        nullable=True,
        comment='最近评估日期'
    )

    # 合作信息
    cooperation_start_date = Column(
        DateTime,
        nullable=True,
        comment='合作开始日期'
    )
    total_transaction_amount = Column(
        Float,
        default=0.0,
        nullable=False,
        comment='累计交易金额'
    )
    total_transaction_count = Column(
        Integer,
        default=0,
        nullable=False,
        comment='累计交易次数'
    )
    last_transaction_date = Column(
        DateTime,
        nullable=True,
        comment='最后交易日期'
    )

    # 财务信息
    bank_name = Column(
        String(100),
        nullable=True,
        comment='开户银行'
    )
    bank_account = Column(
        String(100),
        nullable=True,
        comment='银行账号'
    )
    account_name = Column(
        String(100),
        nullable=True,
        comment='账户名称'
    )
    credit_limit = Column(
        Float,
        nullable=True,
        comment='信用额度'
    )
    payment_terms = Column(
        String(100),
        nullable=True,
        comment='付款条件'
    )

    # 备注信息
    remarks = Column(
        Text,
        nullable=True,
        comment='备注'
    )
    tags = Column(
        JSON,
        nullable=True,
        comment='标签'
    )
    attachments = Column(
        JSON,
        nullable=True,
        comment='附件信息'
    )

    # 关系
    products = relationship(
        'SupplierProduct',
        back_populates='supplier',
        lazy='dynamic',
        cascade='all, delete-orphan'
    )
    purchase_orders = relationship(
        'PurchaseOrder',
        back_populates='supplier',
        lazy='dynamic',
        cascade='all, delete-orphan'
    )
    evaluations = relationship(
        'SupplierEvaluation',
        back_populates='supplier',
        lazy='dynamic',
        cascade='all, delete-orphan'
    )

    def __repr__(self) -> str:
        return f'<Supplier {self.name} ({self.code})>'


class SupplierProduct(Base):
    """供应商产品模型"""
    __tablename__ = 'supplier_product'

    supplier_id = Column(
        UUID(as_uuid=True),
        ForeignKey('supplier.id', ondelete='CASCADE'),
        nullable=False,
        index=True,
        comment='供应商ID'
    )
    product_name = Column(
        String(200),
        nullable=False,
        comment='产品名称'
    )
    product_code = Column(
        String(100),
        nullable=False,
        index=True,
        comment='产品编码'
    )
    product_category = Column(
        String(100),
        nullable=True,
        comment='产品类别'
    )
    product_specification = Column(
        Text,
        nullable=True,
        comment='产品规格'
    )
    unit = Column(
        String(50),
        nullable=True,
        comment='计量单位'
    )
    unit_price = Column(
        Float,
        nullable=True,
        comment='单价'
    )
    currency = Column(
        String(10),
        nullable=True,
        default='CNY',
        comment='货币'
    )
    min_order_quantity = Column(
        Integer,
        nullable=True,
        comment='最小起订量'
    )
    delivery_lead_time = Column(
        Integer,
        nullable=True,
        comment='交货周期（天）'
    )
    quality_standard = Column(
        String(200),
        nullable=True,
        comment='质量标准'
    )
    certification = Column(
        JSON,
        nullable=True,
        comment='产品认证'
    )
    is_active = Column(
        Boolean,
        default=True,
        nullable=False,
        comment='是否有效'
    )
    remarks = Column(
        Text,
        nullable=True,
        comment='备注'
    )

    # 关系
    supplier = relationship(
        'Supplier',
        back_populates='products',
        lazy='selectin'
    )

    def __repr__(self) -> str:
        return f'<SupplierProduct {self.product_name} ({self.product_code})>'


class SupplierEvaluation(Base):
    """供应商评估记录模型"""
    __tablename__ = 'supplier_evaluation'

    supplier_id = Column(
        UUID(as_uuid=True),
        ForeignKey('supplier.id', ondelete='CASCADE'),
        nullable=False,
        index=True,
        comment='供应商ID'
    )
    evaluation_date = Column(
        DateTime,
        nullable=False,
        comment='评估日期'
    )
    evaluator_id = Column(
        UUID(as_uuid=True),
        ForeignKey('user.id'),
        nullable=False,
        comment='评估人ID'
    )
    evaluation_type = Column(
        String(50),
        nullable=False,
        comment='评估类型（periodic:定期, transaction:交易后, spot:抽查）'
    )

    # 评分
    quality_score = Column(
        Float,
        nullable=False,
        comment='质量评分（0-5）'
    )
    delivery_score = Column(
        Float,
        nullable=False,
        comment='交付评分（0-5）'
    )
    service_score = Column(
        Float,
        nullable=False,
        comment='服务评分（0-5）'
    )
    price_score = Column(
        Float,
        nullable=False,
        comment='价格评分（0-5）'
    )
    overall_score = Column(
        Float,
        nullable=False,
        comment='综合评分'
    )

    # 详细评价
    strengths = Column(
        Text,
        nullable=True,
        comment='优势'
    )
    weaknesses = Column(
        Text,
        nullable=True,
        comment='不足'
    )
    improvement_suggestions = Column(
        Text,
        nullable=True,
        comment='改进建议'
    )
    evaluation_result = Column(
        String(50),
        nullable=False,
        comment='评估结果（excellent:优秀, good:良好, qualified:合格, poor:不合格）'
    )
    follow_up_actions = Column(
        Text,
        nullable=True,
        comment='跟进措施'
    )
    next_evaluation_date = Column(
        DateTime,
        nullable=True,
        comment='下次评估日期'
    )

    attachments = Column(
        JSON,
        nullable=True,
        comment='评估附件'
    )
    remarks = Column(
        Text,
        nullable=True,
        comment='备注'
    )

    # 关系
    supplier = relationship(
        'Supplier',
        back_populates='evaluations',
        lazy='selectin'
    )
    evaluator = relationship(
        'User',
        lazy='selectin'
    )

    def __repr__(self) -> str:
        return f'<SupplierEvaluation {self.evaluation_date} - {self.evaluation_result}>'