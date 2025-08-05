/**
 * 中国地图数据加载器
 * 提供中国地图的GeoJSON数据和省份名称映射
 */

// 省份名称标准化映射
const PROVINCE_NAME_MAP = {
    '北京市': '北京', '天津市': '天津', '上海市': '上海', '重庆市': '重庆',
    '河北省': '河北', '山西省': '山西', '辽宁省': '辽宁', '吉林省': '吉林',
    '黑龙江省': '黑龙江', '江苏省': '江苏', '浙江省': '浙江', '安徽省': '安徽',
    '福建省': '福建', '江西省': '江西', '山东省': '山东', '河南省': '河南',
    '湖北省': '湖北', '湖南省': '湖南', '广东省': '广东', '海南省': '海南',
    '四川省': '四川', '贵州省': '贵州', '云南省': '云南', '陕西省': '陕西',
    '甘肃省': '甘肃', '青海省': '青海', '台湾省': '台湾',
    '内蒙古自治区': '内蒙古', '广西壮族自治区': '广西', '西藏自治区': '西藏',
    '宁夏回族自治区': '宁夏', '新疆维吾尔自治区': '新疆',
    '香港特别行政区': '香港', '澳门特别行政区': '澳门'
};

// 中国地图数据加载器
class ChinaMapLoader {
    constructor() {
        this.mapData = null;
        this.isLoaded = false;
    }

    // 加载中国地图数据
    async loadChinaMap() {
        if (this.isLoaded && this.mapData) {
            return this.mapData;
        }

        try {
            // 尝试从多个数据源加载地图数据
            const dataSources = [
                'https://geo.datav.aliyun.com/areas_v3/bound/100000_full.json',
                'https://unpkg.com/echarts@5/map/json/china.json',
                'https://cdn.jsdelivr.net/npm/echarts@5/map/json/china.json'
            ];

            for (const url of dataSources) {
                try {
                    console.log(`尝试从 ${url} 加载地图数据...`);
                    const response = await fetch(url);
                    
                    if (response.ok) {
                        const data = await response.json();
                        this.mapData = data;
                        this.isLoaded = true;
                        console.log('地图数据加载成功');
                        return data;
                    }
                } catch (error) {
                    console.warn(`从 ${url} 加载失败:`, error);
                    continue;
                }
            }

            // 如果所有数据源都失败，使用简化的备用数据
            console.warn('所有地图数据源加载失败，使用备用数据');
            return this.getFallbackMapData();

        } catch (error) {
            console.error('地图数据加载失败:', error);
            return this.getFallbackMapData();
        }
    }

    // 获取备用地图数据（简化版）
    getFallbackMapData() {
        return {
            type: "FeatureCollection",
            features: [
                {
                    type: "Feature",
                    properties: { name: "北京" },
                    geometry: { type: "Polygon", coordinates: [[[116.4, 39.9], [116.5, 39.9], [116.5, 40.0], [116.4, 40.0], [116.4, 39.9]]] }
                },
                {
                    type: "Feature", 
                    properties: { name: "上海" },
                    geometry: { type: "Polygon", coordinates: [[[121.4, 31.2], [121.5, 31.2], [121.5, 31.3], [121.4, 31.3], [121.4, 31.2]]] }
                }
                // 这里可以添加更多省份的简化数据
            ]
        };
    }

    // 标准化省份名称
    normalizeProvinceName(name) {
        // 移除常见后缀
        let cleanName = name.replace(/[省市区]/g, '')
                           .replace(/自治区/g, '')
                           .replace(/特别行政区/g, '')
                           .replace(/维吾尔/g, '')
                           .replace(/壮族/g, '')
                           .replace(/回族/g, '');

        // 使用映射表
        return PROVINCE_NAME_MAP[name] || cleanName || name;
    }

    // 注册地图到ECharts
    async registerChinaMap() {
        try {
            const mapData = await this.loadChinaMap();
            if (mapData && typeof echarts !== 'undefined') {
                echarts.registerMap('china', mapData);
                console.log('中国地图注册成功');
                return true;
            }
            return false;
        } catch (error) {
            console.error('地图注册失败:', error);
            return false;
        }
    }
}

// 全局地图加载器实例
window.chinaMapLoader = new ChinaMapLoader();

// 便捷函数：加载并注册中国地图
window.loadChinaMap = async function() {
    return await window.chinaMapLoader.registerChinaMap();
};

// 便捷函数：标准化省份名称
window.normalizeProvinceName = function(name) {
    return window.chinaMapLoader.normalizeProvinceName(name);
};

console.log('中国地图数据加载器已初始化');
