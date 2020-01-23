// 云函数入口文件
const cloud = require('wx-server-sdk')
cloud.init()
// 云函数入口函数
exports.main = async (event, context) => {
  let {
    type,
    imgUrl
  } = event
  switch (type) {
    case 'idCard':
      {
        // 识别身份证
        console.log('aaaa')
        return idCard(imgUrl)
      }
    case 'bankCard':
      {
        // 识别银行卡
        return bankCard(imgUrl)
      }
    default:
      {
        return
      }
  }
}
//识别身份证
async function idCard(imgUrl) {
  try {
    const result = await cloud.openapi.ocr.idcard({
      type: 'photo',
      imgUrl: imgUrl
    })
    console.log('resultt', result)
    return result
  } catch (err) {
    console.log(err)
    return err
  }
}
//识别银行卡
async function bankCard(imgUrl) {
  try {
    const result = await cloud.openapi.ocr.bankcard({
      type: 'photo',
      imgUrl: imgUrl
    })
    console.log(result)
    return result
  } catch (err) {
    console.log(err)
    return err
  }
}