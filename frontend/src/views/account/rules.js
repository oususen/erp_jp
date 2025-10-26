export default {
  username: [{ required: true, message: 'ユーザー名を入力してください', trigger: 'change' }],
  name: [{ required: true, message: '名称を入力してください', trigger: 'change' }],
  phone: [
    { max: 32, message: '最大長を超えています（32）', trigger: 'change' },
  ],
  email: [
    { max: 256, message: '最大長を超えています（256）', trigger: 'change' },
  ],
  sex: [{ required: true, message: '性別を選択してください', trigger: 'change' }],
}