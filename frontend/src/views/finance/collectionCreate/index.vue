<template>
  <div>
    <a-card title="入金伝票作成">
      <a-button slot="extra" type="primary" ghost @click="() => { this.$router.go(-1); }"> <a-icon
          type="left" />戻る</a-button>
      <a-spin :spinning="loading">
        <a-form-model ref="form" :model="form" :rules="rules" :label-col="{ span: 8 }" :wrapper-col="{ span: 16 }">
          <a-row>
            <a-col :span="6" style="width: 320px;">
              <a-form-model-item prop="number" label="入金コード">
                <a-input v-model="form.number" />
              </a-form-model-item>
            </a-col>
            <a-col :span="6" style="width: 320px;">
              <a-form-model-item prop="client" label="顧客">
                <a-select v-model="form.client" style="width: 100%">
                  <a-select-option v-for="item in clientArrearsItems" :key="item.id" :value="item.id">
                    {{ item.name }}
                  </a-select-option>
                </a-select>
              </a-form-model-item>
            </a-col>
            <a-col :span="6" style="width: 320px;">
              <a-form-model-item prop="handler" label="担当者">
                <a-select v-model="form.handler" style="width: 100%">
                  <a-select-option v-for="item in handlerItems" :key="item.id" :value="item.id">
                    {{ item.name }}
                  </a-select-option>
                </a-select>
              </a-form-model-item>
            </a-col>
            <a-col :span="6" style="width: 320px;">
              <a-form-model-item prop="handle_time" label="処理日">
                <a-date-picker v-model="form.handle_time" valueFormat="YYYY-MM-DD" style="width: 100%" />
              </a-form-model-item>
            </a-col>
            <a-col :span="6" style="width: 320px;">
              <a-form-model-item prop="discount_amount" label="割引金金額">
                <a-input-number v-model="form.discount_amount" style="width: 100%;" />
              </a-form-model-item>
            </a-col>
            <a-col :span="6" style="width: 320px;">
              <a-form-model-item prop="remark" label="備考">
                <a-input v-model="form.remark" allowClear />
              </a-form-model-item>
            </a-col>
          </a-row>
        </a-form-model>
        <div>
          <a-row gutter="16">
            <a-space>
              <a-button type="primary" @click="handelAddAcount">請求先アカウント新規登録する</a-button>
            </a-space>
          </a-row>
          <div style="margin-top: 16px;">
            <a-table rowKey="id" size="middle" :columns="columnsAccount" :data-source="accountsData" :pagination="false">
              <div slot="account" slot-scope="value, item, index">
                <a-select v-if="!item.isTotal" v-model="item.account" style="width: 100%"
                  @change="(value) => changeAccount(value, item, index)">
                  <a-select-option v-for="Account in accountsItems" :key="Account.id" :value="Account.id">
                    {{ Account.name }}
                  </a-select-option>
                </a-select>
              </div>
              <div slot="collection_amount" slot-scope="value, item, index">
                <div v-if="item.isTotal">{{ value }}</div>
                <a-input-number v-else style="width: 100%" v-model="item.collection_amount" :min="0"
                  :precision="2"></a-input-number>
              </div>
              <div slot="action" slot-scope="value, item, index">
                <a-button-group v-if="!item.isTotal" size="small">
                  <a-button type="danger" @click="removeAccount(item)">削除</a-button>
                </a-button-group>
              </div>
            </a-table>
          </div>
        </div>
      </a-spin>
      <div style="width: 100%;display: flex;justify-content: center;">
        <div style="margin-top: 32px;">
          <a-popconfirm title="本当に保存しますか??" @confirm="create">
            <a-button type="primary" :loading="loading">保存</a-button>
          </a-popconfirm>
        </div>
      </div>

    </a-card>
  </div>
</template>

<script>
import moment from 'moment';
import { getCollectionOrderNumber } from '@/api/data'
import { collectionOrderCreate } from '@/api/finance';
import { clientArrearsOption, userOption, accountsOption } from '@/api/option'
import NP from 'number-precision'

export default {
  components: {
  },
  data() {
    return {
      description: '新規登録',
      warehouseItems: [],
      handlerItems: [],
      clientArrearsItems: [],
      accountsItems: [],
      materialsSelectModalVisible: false,
      loading: false,
      model: {},
      form: {},
      rules: {
        number: [
          { required: true, message: 'コードを入力してください', trigger: 'change' },
        ],
        client: [
          { required: true, message: '顧客を選択してください', trigger: 'change' }
        ],
        handler: [
          { required: true, message: '担当者ーを選択してください', trigger: 'change' }
        ],
        handle_time: [
          { required: true, message: '処理日を選択してください', trigger: 'change' },
        ],
        discount_amount: [
          { pattern: new RegExp(/^\d{0,14}(?:\.\d{0,2})?$/), message: '割引金金金額の形式が不正です', trigger: 'change' }
        ],
      },
      columns: [
        {
          title: '連番',
          dataIndex: 'index',
          key: 'index',
          width: 45,
          customRender: (value, item, index) => {
            return item.isTotal ? '合計' : (index + 1)
          },
        },
        {
          title: '名称',
          dataIndex: 'name',
          key: 'name',
          width: 150,
        },
        {
          title: 'コード',
          dataIndex: 'number',
          key: 'number',
          width: 150,
        },
        {
          title: '仕様',
          dataIndex: 'spec',
          key: 'spec',
          width: 150,
        },
        {
          title: '単位',
          dataIndex: 'unit',
          key: 'unit',
          width: 80,
        },
        {
          title: '購入数数数量',
          dataIndex: 'purchase_quantity',
          key: 'purchase_quantity',
          width: 120,
          scopedSlots: { customRender: 'purchase_quantity' },
        },
        {
          title: '購買単価（円）',
          dataIndex: 'purchase_price',
          key: 'purchase_price',
          width: 120,
          scopedSlots: { customRender: 'purchase_price' },
        },
        {
          title: '金金額',
          dataIndex: 'totalAmount',
          key: 'totalAmount',
          width: 200,
          customRender: (value, item) => {
            if (item.isTotal) return value;
            value = NP.times(item.purchase_quantity, item.purchase_price);
            return item.id ? NP.round(value, 2) : ''
          },
        },
        {
          title: '操作',
          dataIndex: 'action',
          key: 'action',
          width: 80,
          scopedSlots: { customRender: 'action' },
        },
      ],
      materialItems: [],
      columnsAccount: [
        {
          title: '連番',
          dataIndex: 'index',
          key: 'index',
          width: 45,
          customRender: (value, item, index) => {
            return item.isTotal ? '合計' : (index + 1)
          },
        },
        {
          title: '決済口座',
          dataIndex: 'account',
          key: 'account',
          width: 200,
          scopedSlots: { customRender: 'account' },
        },
        {
          title: '支払いい金金金額',
          dataIndex: 'collection_amount',
          key: 'collection_amount',
          width: 200,
          scopedSlots: { customRender: 'collection_amount' },
        },
        {
          title: '操作',
          dataIndex: 'action',
          key: 'action',
          width: 80,
          scopedSlots: { customRender: 'action' },
        },
      ],
      collection_account_items: [],
    }
  },
  computed: {
    goodsData() {
      // データデータ統計合計
      let totalQuantity = 0,
        totalAmount = 0;
      for (let item of this.materialItems) {
        totalQuantity = NP.plus(totalQuantity, item.purchase_quantity);
        let amount = NP.times(item.purchase_quantity, item.purchase_price);
        totalAmount = NP.plus(totalAmount, amount);
      }
      return [
        ...this.materialItems,
        {
          id: '-1',
          isTotal: true,
          name: '',
          purchase_quantity: totalQuantity,
          totalAmount: totalAmount,
        },
      ];
    },
    accountsData() {
      // データデータ統計合計
      let totalAmount = 0;
      for (let item of this.collection_account_items) {
        totalAmount = NP.plus(totalAmount, item.collection_amount);
      }
      return [
        ...this.collection_account_items,
        {
          id: '-1',
          isTotal: true,
          collection_amount: totalAmount,
        },
      ];
    },
  },
  methods: {
    moment,
    initData() {
      this.resetForm();
      userOption({ page_size: 999999, is_active: true }).then(data => {
        this.handlerItems = data.results;
      });
      clientArrearsOption({ page_size: 999999, is_active: true }).then(data => {
        this.clientArrearsItems = data.results;
      });
      accountsOption({ page_size: 999999, is_active: true }).then(data => {
        this.accountsItems = data.results;
      });
    },
    handelAddAcount() {
      this.collection_account_items.push({
        id: this.collection_account_items.length + 1,
        account: '',
        collection_amount: 0
      });
    },
    removeAccount(item) {
      this.collection_account_items = this.$functions.removeItem(this.collection_account_items, item);
    },
    changeAccount(value, item, idx) {
      let count = this.collection_account_items.filter((_item) => {
        return _item.account == value;
      })
      if (count.length > 1) {
        this.$message.warn('決済口座変更済み!');
        this.collection_account_items[idx].account = '';
      }
    },
    openMaterialModal() {
      if (!this.form.warehouse) {
        this.$message.warn('最初に入庫を選択してください。');
        return false;
      }
      this.materialsSelectModalVisible = true;
    },
    onSelectMaterial(item) {
      let index = this.materialItems.findIndex(_item => _item.id == item.id);
      if (index != -1) {
        this.$message.warn('商品はすでに存在します');
        return
      }
      this.materialItems = this.$functions.insertItem(this.materialItems, {
        id: item.id,
        goods: item.goods,
        number: item.goods_number,
        name: item.goods_name,
        spec: item.goods_spec,
        unit: item.unit_name,
        purchase_quantity: 1,
        purchase_price: 0,
        total_quantity: item.total_quantity
      });
    },
    removeMaterial(item) {
      this.materialItems = this.$functions.removeItem(this.materialItems, item);
    },
    create() {
      this.$refs.form.validate(async (valid) => {
        if (valid) {
          let ifHasEmptyAccounts = false;

          this.collection_account_items.map(item => {
            if (!item.account || item.collection_amount === '' || item.collection_amount === null) {
              ifHasEmptyAccounts = true;
            }
          })
          if (ifHasEmptyAccounts) {
            this.$message.warn('決済口座情報を完全に入力してください');
            return false
          }
          this.loading = true;
          let formData = {
            ...this.form,
            collection_account_items: this.collection_account_items.map(item => {
              delete item.id
              return item
            })
          };
          collectionOrderCreate(formData).then(data => {
            this.$message.success('作成成功');
            this.$router.push({ path: '/finance/collection' });
          }).finally(() => {
            this.loading = false;
          });
        }
      });
    },
    resetForm() {
      this.form = {};
      getCollectionOrderNumber().then(data => {
        this.form = { number: data.number }
        this.form.number = 'SK'+this.form.number.slice(2)
      })
      this.materialItems = [];
      this.handelAddAcount();
    },
  },
  mounted() {
    this.initData();
  }
}
</script>