import sys
sys.path.insert(0, "/code/python")
for item in sys.path:
    print(item)
import os

# if os.path.isdir("/code/python"):
#     print("Directory exists.")
#     try:
#         items = os.listdir("/code/python")
#         print("Directory contents:")
#         for item in items:
#             print(item)
#     except OSError as e:
#         print(f"Error listing directory: {e}")
# else:
#     print("Directory does not exist.")

from importlib.metadata import distributions
def get_installed_packages():
    return [
        (dist.metadata["Name"], dist.version)
        for dist in distributions()
    ]
# 使用示例
packages = get_installed_packages()
for name, version in packages:
    print(f"{name}=={version}")

# from mcp.server.fastmcp import FastMCP
# from fastmcp.server.fastmcp import FastMCP
from fastmcp import FastMCP
from starlette.applications import Starlette
from starlette.applications import Starlette
from starlette.routing import Mount

mcp = FastMCP("My App")

@mcp.tool()
async def hello() -> str:
    """Return string 'Hello World!'"""
    print("hello tool called")
    return f"Hello World!"
@mcp.tool(
    name="list_supported_crs",
    description="列出所有支持的坐标系统",
)
async def list_supported_crs() -> str:
    """列出所有支持的坐标系统"""
    return (
        "支持的坐标系统格式:\n\n" +
        "1. EPSG代码格式:\n" +
        "   - 示例: EPSG:4326 (WGS84)\n" +
        "   - 示例: EPSG:3857 (Web墨卡托投影)\n\n" +
        "2. WKT格式:\n" +
        "   - 地理坐标系示例:\n" +
        "     GEOGCS[\"WGS 84\",DATUM[\"WGS_1984\",SPHEROID[\"WGS 84\",6378137,298.257223563]],PRIMEM[\"Greenwich\",0],UNIT[\"degree\",0.0174532925199433]]\n\n" +
        "   - 投影坐标系示例:\n" +
        "     PROJCS[\"WGS 84 / UTM zone 50N\",GEOGCS[\"WGS 84\",...],PROJECTION[\"Transverse_Mercator\"],PARAMETER[\"latitude_of_origin\",0],PARAMETER[\"central_meridian\",117],UNIT[\"metre\",1]]\n\n" +
        "3. Proj格式:\n" +
        "   - WGS84示例:\n" +
        "     +proj=longlat +datum=WGS84 +no_defs +type=crs\n\n" +
        "   - Web墨卡托投影示例:\n" +
        "     +proj=merc +a=6378137 +b=6378137 +lat_ts=0 +lon_0=0 +x_0=0 +y_0=0 +k=1 +units=m +no_defs"
    )
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b
@mcp.tool(
    name="transform_coordinates",
    description="在不同坐标系统之间转换坐标，支持EPSG、WKT和Proj格式的坐标系统。\n注意：坐标列表不能为空。",
)
async def transform_coordinates(
    source_crs: str,
    target_crs: str
) -> str:
    """
    处理坐标转换请求。
    
    参数:
        source_crs: 源坐标系统。
        target_crs: 目标坐标系统。
        coordinates: 要转换的坐标列表，每个坐标包含x和y值。列表不能为空。

    返回:
    """
    # transformer = CoordinateTransformer()

    return "源坐标系统{}转换为目标坐标系统{}。".format(source_crs, target_crs)
app = Starlette(
    routes=[
        Mount('/', app=mcp.sse_app()),
    ]
)

if __name__ == "__main__":
    print(uvicorn.__version__)
    uvicorn.run(app, host="0.0.0.0", port=8080)