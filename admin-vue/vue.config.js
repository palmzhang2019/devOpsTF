const { defineConfig } = require('@vue/cli-service');

module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    proxy: {
      '/forgejo': {
        target: 'http://127.0.0.1:3000', // 目标服务器
        changeOrigin: true, // 是否修改请求的主机头
        pathRewrite: { '^/forgejo': '/api' }, // 可选：重写路径
      },
      '/trello': {
        target: 'https://api.trello.com', // 目标服务器
        changeOrigin: true, // 是否修改请求的主机头
        pathRewrite: { '^/trello': '/1' }, // 可选：重写路径
      },
      '/local': {
        target: 'http://127.0.0.1:8000', // 目标服务器
        changeOrigin: true, // 是否修改请求的主机头
        pathRewrite: { '^/local': '' }, // 可选：重写路径
      }
    },
  },
});
