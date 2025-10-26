export default {
  name: [
    { required: true, message: 'ロール名を入力してください', trigger: 'change' },
    { max: 64, message: '最大長を超えています（64）', trigger: 'change' },
  ],
  remark: [{ max: 256, message: '最大長を超えています（256）', trigger: 'change' }],
}