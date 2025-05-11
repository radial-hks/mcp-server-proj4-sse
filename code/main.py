from mcp.server.fastmcp import FastMCP
from starlette.applications import Starlette
from starlette.routing import Mount
from typing import List, Dict, Any
from core.transformation import CoordinateTransformer # Assuming core.transformation is in the same directory level

mcp = FastMCP("Coordinate Transform App")

TRANSFORM_COORDINATES_INPUT_SCHEMA = {
    "type": "object",
    "properties": {
        "source_crs": {
            "type": "string",
            "description": "源坐标系统，支持以下格式：\n1. EPSG代码 (如：EPSG:4326)\n2. WKT格式 (如：GEOGCS[\"WGS 84\",DATUM[...]])\n3. Proj格式 (如：+proj=longlat +datum=WGS84)",
        },
        "target_crs": {
            "type": "string",
            "description": "目标坐标系统，支持以下格式：\n1. EPSG代码 (如：EPSG:4326)\n2. WKT格式 (如：GEOGCS[\"WGS 84\",DATUM[...]])\n3. Proj格式 (如：+proj=longlat +datum=WGS84)",
        },
        "coordinates": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "x": {"type": "number"},
                    "y": {"type": "number"},
                },
                "required": ["x", "y"]
            },
            "minItems": 1,
        }
    },
    "required": ["source_crs", "target_crs", "coordinates"],
}

LIST_SUPPORTED_CRS_INPUT_SCHEMA = {
    "type": "object",
    "properties": {},
}

@mcp.tool(
    name="transform_coordinates",
    description="在不同坐标系统之间转换坐标，支持EPSG、WKT和Proj格式的坐标系统",
)
async def transform_coordinates(source_crs: str, target_crs: str, coordinates: List[Dict[str, float]]) -> str:
    """处理坐标转换请求"""
    if not all([source_crs, target_crs, coordinates]):
        # FastMCP might handle this based on schema, but explicit check is good.
        # However, FastMCP expects the function to raise an error or return a value.
        # For simplicity, we'll let FastMCP handle missing args based on schema if possible,
        # or rely on the CoordinateTransformer to raise errors for invalid CRS.
        # For now, let's assume valid inputs as per schema.
        pass

    transformer = CoordinateTransformer()
    try:
        transformer.set_source_crs(source_crs)
        transformer.set_target_crs(target_crs)
        transformer.initialize_transformer()

        results_log = []
        for coord in coordinates:
            x, y = coord["x"], coord["y"]
            try:
                trans_x, trans_y = transformer.transform_point(x, y)
                results_log.append(
                    f"输入: ({x}, {y})\n输出: ({trans_x:.8f}, {trans_y:.8f})"
                )
            except ValueError as e:
                results_log.append(
                    f"输入: ({x}, {y})\n错误: {str(e)}"
                )
        
        return f"坐标转换结果 (从 {source_crs} 到 {target_crs}):\n" + "\n".join(results_log)

    except ValueError as e:
        # FastMCP tools should ideally return a string or raise an error that FastMCP can handle.
        # Returning an error message string is one way.
        return f"坐标转换失败: {str(e)}"

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
