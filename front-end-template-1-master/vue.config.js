module.exports = {
    devServer: {
        port: 8082, // 设置前端服务端口为8082，避免与后端冲突
        proxy: {
            '/api': {
                target: 'http://localhost:8081', // 修正代理目标到正确的后端端口
                changeOrigin: true,
                pathRewrite: {
                    '^/api': '', // 移除/api前缀，直接访问根路径
                },
            },
        },
    },
};