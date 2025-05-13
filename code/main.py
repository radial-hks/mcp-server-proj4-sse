from mcp.server.fastmcp import FastMCP
from starlette.applications import Starlette
from starlette.routing import Mount

mcp = FastMCP("Coordinate Transform App")

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