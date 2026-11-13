"""Create categories, products and inventory transaction tables."""

from alembic import op
import sqlalchemy as sa


revision = "0001_catalog_tables"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "categories",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.func.now()),
        sa.UniqueConstraint("name", name="uq_category_name"),
    )
    op.create_index("ix_categories_id", "categories", ["id"])
    op.create_index("ix_categories_name", "categories", ["name"])

    op.create_table(
        "products",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("category_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(150), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("sku", sa.String(64), nullable=False),
        sa.Column("price", sa.Numeric(12, 2), nullable=False),
        sa.Column("discount_price", sa.Numeric(12, 2), nullable=True),
        sa.Column("stock_quantity", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("image_url", sa.String(500), nullable=True),
        sa.Column("brand", sa.String(100), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.func.now()),
        sa.ForeignKeyConstraint(
            ["category_id"], ["categories.id"],
            name="fk_products_category_id",
            ondelete="RESTRICT"
        ),
        sa.UniqueConstraint("sku", name="uq_product_sku"),
        sa.CheckConstraint("price >= 0", name="ck_product_price_nonnegative"),
        sa.CheckConstraint(
            "discount_price IS NULL OR (discount_price >= 0 AND discount_price <= price)",
            name="ck_product_discount_valid"
        ),
        sa.CheckConstraint("stock_quantity >= 0", name="ck_product_stock_nonnegative"),
    )
    op.create_index("ix_products_id", "products", ["id"])
    op.create_index("ix_products_category_id", "products", ["category_id"])
    op.create_index("ix_products_name", "products", ["name"])
    op.create_index("ix_products_sku", "products", ["sku"])

    op.create_table(
        "inventory_transactions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("product_id", sa.Integer(), nullable=False),
        sa.Column("transaction_type", sa.String(10), nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=False),
        sa.Column("previous_stock", sa.Integer(), nullable=False),
        sa.Column("updated_stock", sa.Integer(), nullable=False),
        sa.Column("remarks", sa.String(500), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
        sa.ForeignKeyConstraint(
            ["product_id"], ["products.id"],
            name="fk_inventory_product_id",
            ondelete="CASCADE"
        ),
        sa.CheckConstraint("quantity > 0", name="ck_inventory_quantity_positive"),
        sa.CheckConstraint("previous_stock >= 0", name="ck_inventory_previous_nonnegative"),
        sa.CheckConstraint("updated_stock >= 0", name="ck_inventory_updated_nonnegative"),
    )
    op.create_index("ix_inventory_transactions_id", "inventory_transactions", ["id"])
    op.create_index(
        "ix_inventory_transactions_product_id",
        "inventory_transactions",
        ["product_id"]
    )


def downgrade():
    op.drop_table("inventory_transactions")
    op.drop_table("products")
    op.drop_table("categories")
