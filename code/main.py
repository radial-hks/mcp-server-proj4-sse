from mcp.server.fastmcp import FastMCP
from starlette.applications import Starlette
from starlette.routing import Mount
from typing import List, Dict, Any, Annotated # Add Annotated
from pydantic import BaseModel, Field # Add Field
from core.transformation import CoordinateTransformer # Assuming core.transformation is in the same directory level

mcp = FastMCP("Coordinate Transform App")

# Define Pydantic model for a single coordinate
class CoordinateItem(BaseModel):
    x: Annotated[float, Field(description="X坐标值")]
    y: Annotated[float, Field(description="Y坐标值")]

# @mcp.tool(
#     name="transform_coordinates",
#     description="在不同坐标系统之间转换坐标，支持EPSG、WKT和Proj格式的坐标系统。\n注意：坐标列表不能为空。",
# )
# async def transform_coordinates(
#     source_crs: Annotated[str, Field(description='源坐标系统，支持EPSG、WKT和Proj格式，例如："EPSG:4326" 或 "+proj=longlat +datum=WGS84"')], 
#     target_crs: Annotated[str, Field(description='目标坐标系统，支持EPSG、WKT和Proj格式，例如："EPSG:3857" 或 "+proj=merc +a=6378137 +b=6378137 +lat_ts=0 +lon_0=0 +x_0=0 +y_0=0 +k=1 +units=m +no_defs"')], 
#     coordinates: List[CoordinateItem] # MODIFIED
# ) -> str:
#     """
#     处理坐标转换请求。
    
#     参数:
#         source_crs: 源坐标系统。
#         target_crs: 目标坐标系统。
#         coordinates: 要转换的坐标列表，每个坐标包含x和y值。列表不能为空。

#     返回:
#     """
#     transformer = CoordinateTransformer()
#     try:
#         if not coordinates: # ADDED check
#             return "坐标转换失败: 坐标列表不能为空。"

#         transformer.set_source_crs(source_crs)
#         transformer.set_target_crs(target_crs)
#         transformer.initialize_transformer()
#         # ... (rest of the function logic) ...
#         results_log = []
#         for coord in coordinates:
#             x, y = coord.x, coord.y
#             try:
#                 trans_x, trans_y = transformer.transform_point(x, y)
#                 results_log.append(
#                     f"输入: ({x}, {y})\n输出: ({trans_x:.8f}, {trans_y:.8f})"
#                 )
#             except ValueError as e:
#                 results_log.append(
#                     f"输入: ({x}, {y})\n错误: {str(e)}"
#                 )
        
#         return f"坐标转换结果 (从 {source_crs} 到 {target_crs}):\n" + "\n".join(results_log)

#     except ValueError as e:
#         return f"坐标转换失败: {str(e)}"

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

app = Starlette(
    routes=[
        Mount('/', app=mcp.sse_app()),
    ]
)

# If you need to run this directly using uvicorn, for example:
# import uvicorn
# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)
