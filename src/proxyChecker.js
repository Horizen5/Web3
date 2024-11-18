const axios = require('axios');
const IPInfoCache = require('./ipInfoCache');

class ProxyChecker {
  constructor(config, logger) {
    this.config = config;
    this.logger = logger;
    this.ipCache = new IPInfoCache();
  }

  // 获取代理IP信息
  async getProxyIP(proxy) {
    const cachedIP = this.ipCache.getCachedIP(proxy);
    if (cachedIP) return cachedIP;

    try {
      const response = await axios.get(this.config.ipCheckURL, {
        proxy: this.buildProxyConfig(proxy),
      });
      const ipInfo = response.data;
      this.ipCache.cacheIP(proxy, ipInfo);
      return ipInfo;
    } catch (error) {
      throw new Error('代理IP检查失败');
    }
  }

  // 构建代理配置
  buildProxyConfig(proxy) {
    return proxy && proxy.host
      ? {
          host: proxy.host,
          port: parseInt(proxy.port),
          auth:
            proxy.username && proxy.password
              ? { username: proxy.username, password: proxy.password }
              : undefined,
        }
      : undefined;
  }
}

module.exports = ProxyChecker;
