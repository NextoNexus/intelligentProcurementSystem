"""
供应商管理API路由
"""
from typing import List, Optional, Dict, Any
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_
from sqlalchemy.orm import selectinload

from ..core.database import get_db
from ..core.dependencies import get_current_user, require_role
from ..models.supplier import Supplier, SupplierProduct, SupplierEvaluation
from ..models.user import User
from ..schemas.supplier import (
    SupplierCreate, SupplierUpdate, SupplierResponse, SupplierSimpleResponse,
    SupplierProductCreate, SupplierProductUpdate, SupplierProductResponse,
    SupplierEvaluationCreate, SupplierEvaluationUpdate, SupplierEvaluationResponse
)

router = APIRouter()


# ========== 供应商管理API ==========

@router.get("/", response_model=List[SupplierResponse])
async def get_suppliers(
    skip: int = Query(0, ge=0, description="跳过记录数"),
    limit: int = Query(100, ge=1, le=1000, description="每页记录数"),
    search: Optional[str] = Query(None, description="搜索关键词（名称、编码、联系人）"),
    type: Optional[str] = Query(None, description="按供应商类型过滤"),
    status: Optional[str] = Query(None, description="按状态过滤"),
    min_rating: Optional[float] = Query(None, ge=0.0, le=5.0, description="最低评分"),
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    获取供应商列表

    所有登录用户可用，支持分页、搜索和过滤
    """
    # 构建查询
    query = select(Supplier)

    # 应用过滤条件
    if search:
        search_pattern = f"%{search}%"
        query = query.where(
            (Supplier.name.ilike(search_pattern)) |
            (Supplier.code.ilike(search_pattern)) |
            (Supplier.contact_person.ilike(search_pattern)) |
            (Supplier.company_name.ilike(search_pattern))
        )

    if type:
        query = query.where(Supplier.type == type)

    if status:
        query = query.where(Supplier.status == status)

    if min_rating is not None:
        query = query.where(Supplier.overall_rating >= min_rating)

    # 应用分页
    query = query.offset(skip).limit(limit).order_by(Supplier.created_at.desc())

    # 执行查询
    result = await db.execute(query)
    suppliers = result.scalars().all()

    return suppliers


@router.get("/{supplier_id}", response_model=SupplierResponse)
async def get_supplier(
    supplier_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    获取供应商详情

    所有登录用户可用
    """
    result = await db.execute(
        select(Supplier).where(Supplier.id == supplier_id)
    )
    supplier = result.scalar_one_or_none()

    if not supplier:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="供应商不存在"
        )

    return supplier


@router.post("/", response_model=SupplierResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_role("admin"))])
async def create_supplier(
    supplier_data: SupplierCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    创建新供应商（仅管理员）
    """
    # 检查供应商编码是否已存在
    result = await db.execute(
        select(Supplier).where(Supplier.code == supplier_data.code)
    )
    existing_supplier = result.scalar_one_or_none()
    if existing_supplier:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="供应商编码已存在"
        )

    # 检查工商注册号是否已存在
    if supplier_data.registration_number:
        result = await db.execute(
            select(Supplier).where(Supplier.registration_number == supplier_data.registration_number)
        )
        existing_registration = result.scalar_one_or_none()
        if existing_registration:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="工商注册号已存在"
            )

    # 创建供应商
    supplier = Supplier(**supplier_data.model_dump())

    db.add(supplier)
    await db.commit()
    await db.refresh(supplier)

    return supplier


@router.put("/{supplier_id}", response_model=SupplierResponse, dependencies=[Depends(require_role("admin"))])
async def update_supplier(
    supplier_id: UUID,
    supplier_data: SupplierUpdate,
    db: AsyncSession = Depends(get_db)
):
    """
    更新供应商信息（仅管理员）
    """
    # 获取供应商
    result = await db.execute(
        select(Supplier).where(Supplier.id == supplier_id)
    )
    supplier = result.scalar_one_or_none()

    if not supplier:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="供应商不存在"
        )

    # 检查供应商编码是否已被其他供应商使用
    if supplier_data.code and supplier_data.code != supplier.code:
        result = await db.execute(
            select(Supplier).where(Supplier.code == supplier_data.code)
        )
        existing_supplier = result.scalar_one_or_none()
        if existing_supplier:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="供应商编码已存在"
            )

    # 检查工商注册号是否已被其他供应商使用
    if (supplier_data.registration_number and
        supplier_data.registration_number != supplier.registration_number):
        result = await db.execute(
            select(Supplier).where(Supplier.registration_number == supplier_data.registration_number)
        )
        existing_registration = result.scalar_one_or_none()
        if existing_registration:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="工商注册号已存在"
            )

    # 更新字段
    update_data = supplier_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(supplier, field, value)

    await db.commit()
    await db.refresh(supplier)

    return supplier


@router.delete("/{supplier_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(require_role("admin"))])
async def delete_supplier(
    supplier_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """
    删除供应商（仅管理员）
    """
    # 获取供应商
    result = await db.execute(
        select(Supplier).where(Supplier.id == supplier_id)
    )
    supplier = result.scalar_one_or_none()

    if not supplier:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="供应商不存在"
        )

    # 检查是否有相关采购订单
    # 注意：这里需要检查采购订单模型，暂时跳过
    # 实际项目中需要根据业务逻辑决定是否允许删除

    # 删除供应商
    await db.delete(supplier)
    await db.commit()

    return None


@router.get("/{supplier_id}/products", response_model=List[SupplierProductResponse])
async def get_supplier_products(
    supplier_id: UUID,
    skip: int = Query(0, ge=0, description="跳过记录数"),
    limit: int = Query(100, ge=1, le=1000, description="每页记录数"),
    is_active: Optional[bool] = Query(None, description="按是否有效过滤"),
    category: Optional[str] = Query(None, description="按产品类别过滤"),
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    获取供应商产品列表

    所有登录用户可用
    """
    # 检查供应商是否存在
    result = await db.execute(
        select(Supplier).where(Supplier.id == supplier_id)
    )
    supplier = result.scalar_one_or_none()

    if not supplier:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="供应商不存在"
        )

    # 构建查询
    query = select(SupplierProduct).where(SupplierProduct.supplier_id == supplier_id)

    if is_active is not None:
        query = query.where(SupplierProduct.is_active == is_active)

    if category:
        query = query.where(SupplierProduct.product_category == category)

    # 应用分页
    query = query.offset(skip).limit(limit).order_by(SupplierProduct.product_name)

    # 执行查询
    result = await db.execute(query)
    products = result.scalars().all()

    return products


@router.post("/{supplier_id}/products", response_model=SupplierProductResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_role("admin"))])
async def create_supplier_product(
    supplier_id: UUID,
    product_data: SupplierProductCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    创建供应商产品（仅管理员）
    """
    # 检查供应商是否存在
    result = await db.execute(
        select(Supplier).where(Supplier.id == supplier_id)
    )
    supplier = result.scalar_one_or_none()

    if not supplier:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="供应商不存在"
        )

    # 检查产品编码是否已存在（同一供应商内）
    result = await db.execute(
        select(SupplierProduct).where(
            (SupplierProduct.supplier_id == supplier_id) &
            (SupplierProduct.product_code == product_data.product_code)
        )
    )
    existing_product = result.scalar_one_or_none()
    if existing_product:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="该供应商下产品编码已存在"
        )

    # 创建产品
    product = SupplierProduct(
        supplier_id=supplier_id,
        **product_data.model_dump(exclude={'supplier_id'})
    )

    db.add(product)
    await db.commit()
    await db.refresh(product)

    return product


@router.get("/products/{product_id}", response_model=SupplierProductResponse)
async def get_supplier_product(
    product_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    获取供应商产品详情

    所有登录用户可用
    """
    result = await db.execute(
        select(SupplierProduct).where(SupplierProduct.id == product_id)
    )
    product = result.scalar_one_or_none()

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="产品不存在"
        )

    return product


@router.put("/products/{product_id}", response_model=SupplierProductResponse, dependencies=[Depends(require_role("admin"))])
async def update_supplier_product(
    product_id: UUID,
    product_data: SupplierProductUpdate,
    db: AsyncSession = Depends(get_db)
):
    """
    更新供应商产品信息（仅管理员）
    """
    # 获取产品
    result = await db.execute(
        select(SupplierProduct).where(SupplierProduct.id == product_id)
    )
    product = result.scalar_one_or_none()

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="产品不存在"
        )

    # 检查产品编码是否已被其他产品使用（同一供应商内）
    if product_data.product_code and product_data.product_code != product.product_code:
        result = await db.execute(
            select(SupplierProduct).where(
                (SupplierProduct.supplier_id == product.supplier_id) &
                (SupplierProduct.product_code == product_data.product_code)
            )
        )
        existing_product = result.scalar_one_or_none()
        if existing_product:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="该供应商下产品编码已存在"
            )

    # 更新字段
    update_data = product_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(product, field, value)

    await db.commit()
    await db.refresh(product)

    return product


@router.delete("/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(require_role("admin"))])
async def delete_supplier_product(
    product_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """
    删除供应商产品（仅管理员）
    """
    # 获取产品
    result = await db.execute(
        select(SupplierProduct).where(SupplierProduct.id == product_id)
    )
    product = result.scalar_one_or_none()

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="产品不存在"
        )

    # 删除产品
    await db.delete(product)
    await db.commit()

    return None


@router.get("/{supplier_id}/evaluations", response_model=List[SupplierEvaluationResponse])
async def get_supplier_evaluations(
    supplier_id: UUID,
    skip: int = Query(0, ge=0, description="跳过记录数"),
    limit: int = Query(100, ge=1, le=1000, description="每页记录数"),
    evaluation_type: Optional[str] = Query(None, description="按评估类型过滤"),
    evaluator_id: Optional[UUID] = Query(None, description="按评估人ID过滤"),
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    获取供应商评估记录

    所有登录用户可用
    """
    # 检查供应商是否存在
    result = await db.execute(
        select(Supplier).where(Supplier.id == supplier_id)
    )
    supplier = result.scalar_one_or_none()

    if not supplier:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="供应商不存在"
        )

    # 构建查询
    query = select(SupplierEvaluation).where(SupplierEvaluation.supplier_id == supplier_id)

    if evaluation_type:
        query = query.where(SupplierEvaluation.evaluation_type == evaluation_type)

    if evaluator_id:
        query = query.where(SupplierEvaluation.evaluator_id == evaluator_id)

    # 应用分页
    query = query.offset(skip).limit(limit).order_by(SupplierEvaluation.evaluation_date.desc())

    # 执行查询
    result = await db.execute(query)
    evaluations = result.scalars().all()

    return evaluations


@router.post("/{supplier_id}/evaluations", response_model=SupplierEvaluationResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_role("admin"))])
async def create_supplier_evaluation(
    supplier_id: UUID,
    evaluation_data: SupplierEvaluationCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    创建供应商评估记录（仅管理员）
    """
    # 检查供应商是否存在
    result = await db.execute(
        select(Supplier).where(Supplier.id == supplier_id)
    )
    supplier = result.scalar_one_or_none()

    if not supplier:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="供应商不存在"
        )

    # 检查评估人是否存在
    result = await db.execute(
        select(User).where(User.id == evaluation_data.evaluator_id)
    )
    evaluator = result.scalar_one_or_none()

    if not evaluator:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="评估人不存在"
        )

    # 计算综合评分
    overall_score = (evaluation_data.quality_score +
                    evaluation_data.delivery_score +
                    evaluation_data.service_score +
                    evaluation_data.price_score) / 4

    # 创建评估记录
    evaluation = SupplierEvaluation(
        supplier_id=supplier_id,
        overall_score=overall_score,
        **evaluation_data.model_dump()
    )

    # 更新供应商评分
    supplier.overall_rating = overall_score
    supplier.quality_rating = evaluation_data.quality_score
    supplier.delivery_rating = evaluation_data.delivery_score
    supplier.service_rating = evaluation_data.service_score
    supplier.price_rating = evaluation_data.price_score
    supplier.assessment_date = evaluation_data.evaluation_date

    db.add(evaluation)
    await db.commit()
    await db.refresh(evaluation)

    return evaluation


@router.get("/evaluations/{evaluation_id}", response_model=SupplierEvaluationResponse)
async def get_supplier_evaluation(
    evaluation_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    获取供应商评估详情

    所有登录用户可用
    """
    result = await db.execute(
        select(SupplierEvaluation).where(SupplierEvaluation.id == evaluation_id)
    )
    evaluation = result.scalar_one_or_none()

    if not evaluation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="评估记录不存在"
        )

    return evaluation


@router.put("/evaluations/{evaluation_id}", response_model=SupplierEvaluationResponse, dependencies=[Depends(require_role("admin"))])
async def update_supplier_evaluation(
    evaluation_id: UUID,
    evaluation_data: SupplierEvaluationUpdate,
    db: AsyncSession = Depends(get_db)
):
    """
    更新供应商评估记录（仅管理员）
    """
    # 获取评估记录
    result = await db.execute(
        select(SupplierEvaluation).where(SupplierEvaluation.id == evaluation_id)
    )
    evaluation = result.scalar_one_or_none()

    if not evaluation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="评估记录不存在"
        )

    # 更新字段
    update_data = evaluation_data.model_dump(exclude_unset=True)

    # 如果评分有更新，重新计算综合评分
    if any(key in update_data for key in ['quality_score', 'delivery_score', 'service_score', 'price_score']):
        quality_score = update_data.get('quality_score', evaluation.quality_score)
        delivery_score = update_data.get('delivery_score', evaluation.delivery_score)
        service_score = update_data.get('service_score', evaluation.service_score)
        price_score = update_data.get('price_score', evaluation.price_score)

        overall_score = (quality_score + delivery_score + service_score + price_score) / 4
        update_data['overall_score'] = overall_score

        # 更新供应商评分
        supplier = await db.get(Supplier, evaluation.supplier_id)
        if supplier:
            supplier.overall_rating = overall_score
            supplier.quality_rating = quality_score
            supplier.delivery_rating = delivery_score
            supplier.service_rating = service_score
            supplier.price_rating = price_score
            supplier.assessment_date = evaluation.evaluation_date

    for field, value in update_data.items():
        setattr(evaluation, field, value)

    await db.commit()
    await db.refresh(evaluation)

    return evaluation


@router.delete("/evaluations/{evaluation_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(require_role("admin"))])
async def delete_supplier_evaluation(
    evaluation_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """
    删除供应商评估记录（仅管理员）
    """
    # 获取评估记录
    result = await db.execute(
        select(SupplierEvaluation).where(SupplierEvaluation.id == evaluation_id)
    )
    evaluation = result.scalar_one_or_none()

    if not evaluation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="评估记录不存在"
        )

    # 删除评估记录
    await db.delete(evaluation)
    await db.commit()

    return None


@router.get("/simple/", response_model=List[SupplierSimpleResponse])
async def get_simple_suppliers(
    status: Optional[str] = Query(None, description="按状态过滤"),
    type: Optional[str] = Query(None, description="按供应商类型过滤"),
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    获取简化供应商列表（用于下拉选择等场景）

    所有登录用户可用
    """
    query = select(Supplier).where(Supplier.status == "active")

    if status:
        query = query.where(Supplier.status == status)

    if type:
        query = query.where(Supplier.type == type)

    query = query.order_by(Supplier.name)

    result = await db.execute(query)
    suppliers = result.scalars().all()

    return suppliers