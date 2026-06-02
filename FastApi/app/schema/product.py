from uuid import UUID
from typing import Annotated, Literal, Optional, List

from pydantic import (
    BaseModel,
    Field,
    AnyUrl,
    field_validator,
    model_validator,
    computed_field
)


class Product(BaseModel):

    id: UUID

    sku: Annotated[
        str,
        Field(
            description="Stock Keeping Unit",
            min_length=6,
            max_length=30,
            examples=["734-hjd-768-123"]
        )
    ]

    name: Annotated[
        str,
        Field(
            title="Product Name",
            description="Product name",
            min_length=1,
            max_length=100,
            examples=["Wireless Mouse"]
        )
    ]

    description: Annotated[
        str,
        Field(
            description="Product description",
            min_length=1,
            max_length=500,
            examples=[
                "A high-precision wireless mouse with ergonomic design."
            ]
        )
    ]

    price: Annotated[
        float,
        Field(
            description="Product price",
            gt=0,
            examples=[29.99]
        )
    ]

    category: Annotated[
        str,
        Field(
            description="Product category",
            min_length=1,
            max_length=100,
            examples=["Electronics"]
        )
    ]

    brand: Annotated[
        str,
        Field(
            description="Product brand",
            min_length=1,
            max_length=100,
            examples=["Logitech"]
        )
    ]

    currency: Literal["INR"] = Field(
        default="INR",
        description="Currency code",
        examples=["INR"]
    )

    discount_percent: Annotated[
        float,
        Field(
            description="Discount percentage",
            ge=0,
            le=100,
            examples=[10.0]
        )
    ]

    stock: Annotated[
        int,
        Field(
            description="Available stock quantity",
            ge=0,
            examples=[100]
        )
    ]

    is_active: bool = Field(
        default=True,
        description="Product availability status",
        examples=[True]
    )

    rating: Annotated[
        float,
        Field(
            description="Average product rating",
            ge=0,
            le=5,
            examples=[4.5]
        )
    ]

    tags: Annotated[
        Optional[List[str]],
        Field(
            description="Up to 10 tags",
            examples=[["wireless", "mouse", "logitech"]],
            max_length=10
        )
    ] = None

    image_url: Optional[AnyUrl] = Field(
        default=None,
        description="URL of the product image",
        examples=["https://example.com/images/wireless-mouse.jpg"]
    )

    @field_validator("sku", mode="after")
    @classmethod
    def validate_sku(cls, value: str):

        if "-" not in value:
            raise ValueError(
                "SKU must have '-' separated segments"
            )

        last = value.split("-")[-1]

        if not (len(last) == 3 and last.isdigit()):
            raise ValueError(
                "Last segment of SKU must be exactly 3 digits"
            )

        return value
    
    @model_validator(mode="after")
    @classmethod
    def validate_business_rules(cls , model: "Product"):
        if model.stock == 0 and model.is_active:
            raise ValueError(
                "Product cannot be active if stock is zero"
            )                                             
        
        return model
    
    @computed_field
    @property
    def discounted_price(self) -> float:
        return round(self.price * (1 - self.discount_percent / 100), 2)
    