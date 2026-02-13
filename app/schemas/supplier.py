"""
供应商相关的Pydantic模型
"""
from typing import Optional, List, Dict, Any
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field


class SupplierBase(BaseModel):
    """供应商基础模型"""
    name: str = Field(..., max_length=200, description="供应商名称")
    code: str = Field(..., max_length=50, description="供应商编码")
    type: str = Field(default="general", description="供应商类型（general:普通, strategic:战略, key:关键）")
    status: str = Field(default="active", description="状态（active:活跃, inactive:不活跃, suspended:暂停, blacklisted:黑名单）")

    # 联系信息
    contact_person: Optional[str] = Field(None, max_length=100, description="联系人")
    contact_phone: Optional[str] = Field(None, max_length=20, description="联系电话")
    contact_email: Optional[str] = Field(None, max_length=255, description="联系邮箱")
    contact_address: Optional[str] = Field(None, description="联系地址")

    # 公司信息
    company_name: Optional[str] = Field(None, max_length=200, description="公司名称")
    registration_number: Optional[str] = Field(None, max_length=100, description="工商注册号")
    tax_number: Optional[str] = Field(None, max_length=100, description="税务登记号")
    business_scope: Optional[str] = Field(None, description="经营范围")
    registered_capital: Optional[float] = Field(None, description="注册资本（万元）")
    established_date: Optional[datetime] = Field(None, description="成立日期")

    # 资质信息
    qualification_level: Optional[str] = Field(None, max_length=50, description="资质等级")
    qualification_certificates: Optional[List[Dict[str, Any]]] = Field(None, description="资质证书信息")
    quality_system: Optional[str] = Field(None, max_length=100, description="质量体系认证")
    industry_certifications: Optional[List[Dict[str, Any]]] = Field(None, description="行业认证")

    # 财务信息
    bank_name: Optional[str] = Field(None, max_length=100, description="开户银行")
    bank_account: Optional[str] = Field(None, max_length=100, description="银行账号")
    account_name: Optional[str] = Field(None, max_length=100, description="账户名称")
    credit_limit: Optional[float] = Field(None, description="信用额度")
    payment_terms: Optional[str] = Field(None, max_length=100, description="付款条件")

    # 备注信息
    remarks: Optional[str] = Field(None, description="备注")
    tags: Optional[List[str]] = Field(None, description="标签")


class SupplierCreate(SupplierBase):
    """创建供应商请求模型"""
    pass


class SupplierUpdate(BaseModel):
    """更新供应商请求模型"""
    name: Optional[str] = Field(None, max_length=200, description="供应商名称")
    code: Optional[str] = Field(None, max_length=50, description="供应商编码")
    type: Optional[str] = Field(None, description="供应商类型")
    status: Optional[str] = Field(None, description="状态")

    # 联系信息
    contact_person: Optional[str] = Field(None, max_length=100, description="联系人")
    contact_phone: Optional[str] = Field(None, max_length=20, description="联系电话")
    contact_email: Optional[str] = Field(None, max_length=255, description="联系邮箱")
    contact_address: Optional[str] = Field(None, description="联系地址")

    # 公司信息
    company_name: Optional[str] = Field(None, max_length=200, description="公司名称")
    registration_number: Optional[str] = Field(None, max_length=100, description="工商注册号")
    tax_number: Optional[str] = Field(None, max_length=100, description="税务登记号")
    business_scope: Optional[str] = Field(None, description="经营范围")
    registered_capital: Optional[float] = Field(None, description="注册资本（万元）")
    established_date: Optional[datetime] = Field(None, description="成立日期")

    # 资质信息
    qualification_level: Optional[str] = Field(None, max_length=50, description="资质等级")
    qualification_certificates: Optional[List[Dict[str, Any]]] = Field(None, description="资质证书信息")
    quality_system: Optional[str] = Field(None, max_length=100, description="质量体系认证")
    industry_certifications: Optional[List[Dict[str, Any]]] = Field(None, description="行业认证")

    # 财务信息
    bank_name: Optional[str] = Field(None, max_length=100, description="开户银行")
    bank_account: Optional[str] = Field(None, max_length=100, description="银行账号")
    account_name: Optional[str] = Field(None, max_length=100, description="账户名称")
    credit_limit: Optional[float] = Field(None, description="信用额度")
    payment_terms: Optional[str] = Field(None, max_length=100, description="付款条件")

    # 备注信息
    remarks: Optional[str] = Field(None, description="备注")
    tags: Optional[List[str]] = Field(None, description="标签")


class SupplierResponse(SupplierBase):
    """供应商信息响应模型"""
    id: UUID = Field(..., description="供应商ID")

    # 评估信息
    overall_rating: float = Field(default=0.0, description="综合评分（0-5）")
    quality_rating: float = Field(default=0.0, description="质量评分")
    delivery_rating: float = Field(default=0.0, description="交付评分")
    service_rating: float = Field(default=0.0, description="服务评分")
    price_rating: float = Field(default=0.0, description="价格评分")
    assessment_date: Optional[datetime] = Field(None, description="最近评估日期")

    # 合作信息
    cooperation_start_date: Optional[datetime] = Field(None, description="合作开始日期")
    total_transaction_amount: float = Field(default=0.0, description="累计交易金额")
    total_transaction_count: int = Field(default=0, description="累计交易次数")
    last_transaction_date: Optional[datetime] = Field(None, description="最后交易日期")

    # 附件信息
    attachments: Optional[List[Dict[str, Any]]] = Field(None, description="附件信息")

    # 时间戳
    created_at: Optional[datetime] = Field(None, description="创建时间")
    updated_at: Optional[datetime] = Field(None, description="更新时间")

    class Config:
        from_attributes = True


class SupplierSimpleResponse(BaseModel):
    """简化供应商响应模型（用于下拉选择等场景）"""
    id: UUID = Field(..., description="供应商ID")
    name: str = Field(..., description="供应商名称")
    code: str = Field(..., description="供应商编码")
    type: str = Field(..., description="供应商类型")
    status: str = Field(..., description="状态")
    contact_person: Optional[str] = Field(None, description="联系人")
    contact_phone: Optional[str] = Field(None, description="联系电话")

    class Config:
        from_attributes = True


class SupplierProductBase(BaseModel):
    """供应商产品基础模型"""
    product_name: str = Field(..., max_length=200, description="产品名称")
    product_code: str = Field(..., max_length=100, description="产品编码")
    product_category: Optional[str] = Field(None, max_length=100, description="产品类别")
    product_specification: Optional[str] = Field(None, description="产品规格")
    unit: Optional[str] = Field(None, max_length=50, description="计量单位")
    unit_price: Optional[float] = Field(None, description="单价")
    currency: str = Field(default="CNY", max_length=10, description="货币")
    min_order_quantity: Optional[int] = Field(None, description="最小起订量")
    delivery_lead_time: Optional[int] = Field(None, description="交货周期（天）")
    quality_standard: Optional[str] = Field(None, max_length=200, description="质量标准")
    certification: Optional[List[Dict[str, Any]]] = Field(None, description="产品认证")
    is_active: bool = Field(default=True, description="是否有效")
    remarks: Optional[str] = Field(None, description="备注")


class SupplierProductCreate(SupplierProductBase):
    """创建供应商产品请求模型"""
    supplier_id: UUID = Field(..., description="供应商ID")


class SupplierProductUpdate(BaseModel):
    """更新供应商产品请求模型"""
    product_name: Optional[str] = Field(None, max_length=200, description="产品名称")
    product_code: Optional[str] = Field(None, max_length=100, description="产品编码")
    product_category: Optional[str] = Field(None, max_length=100, description="产品类别")
    product_specification: Optional[str] = Field(None, description="产品规格")
    unit: Optional[str] = Field(None, max_length=50, description="计量单位")
    unit_price: Optional[float] = Field(None, description="单价")
    currency: Optional[str] = Field(None, max_length=10, description="货币")
    min_order_quantity: Optional[int] = Field(None, description="最小起订量")
    delivery_lead_time: Optional[int] = Field(None, description="交货周期（天）")
    quality_standard: Optional[str] = Field(None, max_length=200, description="质量标准")
    certification: Optional[List[Dict[str, Any]]] = Field(None, description="产品认证")
    is_active: Optional[bool] = Field(None, description="是否有效")
    remarks: Optional[str] = Field(None, description="备注")


class SupplierProductResponse(SupplierProductBase):
    """供应商产品响应模型"""
    id: UUID = Field(..., description="产品ID")
    supplier_id: UUID = Field(..., description="供应商ID")
    supplier_name: str = Field(..., description="供应商名称")
    created_at: Optional[datetime] = Field(None, description="创建时间")
    updated_at: Optional[datetime] = Field(None, description="更新时间")

    class Config:
        from_attributes = True


class SupplierEvaluationBase(BaseModel):
    """供应商评估基础模型"""
    evaluation_type: str = Field(..., description="评估类型（periodic:定期, transaction:交易后, spot:抽查）")

    # 评分
    quality_score: float = Field(..., ge=0.0, le=5.0, description="质量评分（0-5）")
    delivery_score: float = Field(..., ge=0.0, le=5.0, description="交付评分（0-5）")
    service_score: float = Field(..., ge=0.0, le=5.0, description="服务评分（0-5）")
    price_score: float = Field(..., ge=0.0, le=5.0, description="价格评分（0-5）")

    # 详细评价
    strengths: Optional[str] = Field(None, description="优势")
    weaknesses: Optional[str] = Field(None, description="不足")
    improvement_suggestions: Optional[str] = Field(None, description="改进建议")
    evaluation_result: str = Field(..., description="评估结果（excellent:优秀, good:良好, qualified:合格, poor:不合格）")
    follow_up_actions: Optional[str] = Field(None, description="跟进措施")
    next_evaluation_date: Optional[datetime] = Field(None, description="下次评估日期")

    # 附件和备注
    attachments: Optional[List[Dict[str, Any]]] = Field(None, description="评估附件")
    remarks: Optional[str] = Field(None, description="备注")


class SupplierEvaluationCreate(SupplierEvaluationBase):
    """创建供应商评估请求模型"""
    supplier_id: UUID = Field(..., description="供应商ID")
    evaluator_id: UUID = Field(..., description="评估人ID")
    evaluation_date: datetime = Field(default_factory=datetime.utcnow, description="评估日期")


class SupplierEvaluationUpdate(BaseModel):
    """更新供应商评估请求模型"""
    evaluation_type: Optional[str] = Field(None, description="评估类型")

    # 评分
    quality_score: Optional[float] = Field(None, ge=0.0, le=5.0, description="质量评分")
    delivery_score: Optional[float] = Field(None, ge=0.0, le=5.0, description="交付评分")
    service_score: Optional[float] = Field(None, ge=0.0, le=5.0, description="服务评分")
    price_score: Optional[float] = Field(None, ge=0.0, le=5.0, description="价格评分")

    # 详细评价
    strengths: Optional[str] = Field(None, description="优势")
    weaknesses: Optional[str] = Field(None, description="不足")
    improvement_suggestions: Optional[str] = Field(None, description="改进建议")
    evaluation_result: Optional[str] = Field(None, description="评估结果")
    follow_up_actions: Optional[str] = Field(None, description="跟进措施")
    next_evaluation_date: Optional[datetime] = Field(None, description="下次评估日期")

    # 附件和备注
    attachments: Optional[List[Dict[str, Any]]] = Field(None, description="评估附件")
    remarks: Optional[str] = Field(None, description="备注")


class SupplierEvaluationResponse(SupplierEvaluationBase):
    """供应商评估响应模型"""
    id: UUID = Field(..., description="评估ID")
    supplier_id: UUID = Field(..., description="供应商ID")
    supplier_name: str = Field(..., description="供应商名称")
    evaluator_id: UUID = Field(..., description="评估人ID")
    evaluator_name: str = Field(..., description="评估人姓名")
    evaluation_date: datetime = Field(..., description="评估日期")
    overall_score: float = Field(..., description="综合评分")
    created_at: Optional[datetime] = Field(None, description="创建时间")
    updated_at: Optional[datetime] = Field(None, description="更新时间")

    class Config:
        from_attributes = True