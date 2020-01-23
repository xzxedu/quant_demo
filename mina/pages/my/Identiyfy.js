Page({
  //身份证
  shenfenzheng() {
    this.photo("shenfenzheng")
  },
  //银行卡
  yinhangka() {
    this.photo("yinhangka")
  },
  //行驶证
  xingshizheng() {
    this.photo("xingshizheng")
  },
  //拍照或者从相册选择要识别的照片
  photo(type) {
    let that = this
    wx.chooseImage({
      count: 1,
      sizeType: ['original', 'compressed'],
      sourceType: ['album', 'camera'],
      success(res) {
        // tempFilePath可以作为img标签的src属性显示图片
        let imgUrl = res.tempFilePaths[0];
        that.uploadImg(type, imgUrl)
      }
    })
  },
  // 上传图片到云存储
  uploadImg(type, imgUrl) {
    let that = this
    wx.cloud.uploadFile({
      cloudPath: 'ocr/' + type + '.png',
      filePath: imgUrl, // 文件路径
      success: res => {
        console.log("上传成功", res.fileID)
        that.getImgUrl(type, res.fileID)
      },
      fail: err => {
        console.log("上传失败", err)
      }
    })
  },
  //获取云存储里的图片url
  getImgUrl(type, imgUrl) {
    let that = this
    wx.cloud.getTempFileURL({
      fileList: [imgUrl],
      success: res => {
        let imgUrl = res.fileList[0].tempFileURL
        console.log("获取图片url成功", imgUrl)
        that.shibie(type, imgUrl)
      },
      fail: err => {
        console.log("获取图片url失败", err)
      }
    })
  },
  //调用云函数，实现OCR识别
  shibie(type, imgUrl) {
    wx.cloud.callFunction({
      name: "ocr",
      data: {
        type: type,
        imgUrl: imgUrl
      },
      success(res) {
        console.log("识别成功", res)
      },
      fail(res) {
        console.log("识别失败", res)
      }
    })
  }
})