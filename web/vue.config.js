module.exports = {
  transpileDependencies: ['vuetify'],
  pwa: {
    workboxOptions: {
      skipWaiting: true
    }
  },
  devServer: {
    compress: true,
    public: 'store-client-nestroia1.c9users.io' // That solved it
  }
}
