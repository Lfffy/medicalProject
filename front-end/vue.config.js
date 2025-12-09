module.exports = {
    devServer: {
        port: 8082, // 设置前端服务端口为8082，避免与后端冲突
        proxy: {
            '/api': {
                target: 'http://localhost:8081', // 修正代理目标到后端端口8081
                changeOrigin: true,
                pathRewrite: {
                    '^/api': '' // 移除/api前缀，避免重复
                }
            },
        },
    },
};