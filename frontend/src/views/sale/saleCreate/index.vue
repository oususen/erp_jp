<template>
  <div>
    <a-card title="販売注文">
      <a-spin :spinning="loading">
        <a-form-model ref="form" :model="form" :rules="rules" :label-col="{ span: 8 }" :wrapper-col="{ span: 16 }">
          <a-row>
            <a-col :span="6" style="width: 320px;">
              <a-form-model-item prop="number" label="販売回数">
                <a-input v-model="form.number" />
              </a-form-model-item>
            </a-col>
            <a-col :span="6" style="width: 320px;">
              <a-form-model-item prop="warehouse" label="入庫">
                <a-select v-model="form.warehouse" style="width: 100%">
                  <a-select-option v-for="item in warehouseItems" :key="item.id" :value="item.id">
                    {{ item.name }}
                  </a-select-option>
                </a-select>
              </a-form-model-item>
            </a-col>
            <a-col :span="6" style="width: 320px;">
              <a-form-model-item prop="client" label="顧客">
                <a-select v-model="form.client" style="width: 100%">
                  <a-select-option v-for="item in clientsItems" :key="item.id" :value="item.id">
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
              <a-form-model-item prop="remark" label="備考">
                <a-input v-model="form.remark" allowClear />
              </a-form-model-item>
            </a-col>
          </a-row>
        </a-form-model>

        <a-divider orientation="left">商品情報</a-divider>

        <div>
          <a-row gutter="16">
            <a-space>
              <a-button type="primary" @click="openMaterialModal">商品を追加</a-button>
            </a-space>
          </a-row>
          <div style="margin-top: 16px;">
            <a-table rowKey="id" size="middle" :columns="columns" :data-source="goodsData" :pagination="false">
              <div slot="sales_quantity" slot-scope="value, item, index">
                <div v-if="item.isTotal">{{ value }}</div>
                <a-input-number v-else v-model="item.sales_quantity" :min="0" size="small"></a-input-number>
              </div>
              <div slot="sales_price" slot-scope="value, item, index">
                <a-input-number v-if="!item.isTotal" v-model="item.sales_price" :min="0" size="small"></a-input-number>
              </div>
              <div slot="tax" slot-scope="value, item, index">
                <div v-if="!item.isTotal" style="display: flex;flex-direction: row;align-items: center">
                  <a-input-number v-model="item.tax" :min="0" size="small" style="width: 60px;"></a-input-number>
                  <a>%</a>
                </div>

              </div>
              <div slot="action" slot-scope="value, item, index">
                <a-button-group v-if="!item.isTotal" size="small">
                  <a-button type="danger" @click="removeMaterial(item)">削除</a-button>
                </a-button-group>
              </div>
            </a-table>
          </div>
        </div>
        <a-divider orientation="left">請求書情報</a-divider>
        <div>
          <a-row gutter="16">
            <a-col :span="4">
              <a-form-model-item prop="discount" label="全伝票割引" :label-col="{ span: 24 }" :wrapper-col="{ span: 24 }">
                <a-input-number v-model="form.discount" style="width: 100%;" />
              </a-form-model-item>
            </a-col>

            <a-col :span="4">
              <a-form-model-item prop="other_amount" label="そのその他費用" :label-col="{ span: 24 }" :wrapper-col="{ span: 24 }">
                <a-input-number v-model="form.other_amount" style="width: 100%;" />
              </a-form-model-item>
            </a-col>
            <a-col :span="4">
              <a-form-model-item label="合計金金金額（円）" :label-col="{ span: 24 }" :wrapper-col="{ span: 24 }">
                <a-input-number :value="totalAmount" :disabled="true" style="width: 100%;" />
              </a-form-model-item>
            </a-col>

            <a-col :span="4">
              <a-form-model-item label="決済口座" :label-col="{ span: 24 }" :wrapper-col="{ span: 24 }">
                <a-select v-model="sales_account_item.account" style="width: 100%">
                  <a-select-option v-for="Account in accountsItems" :key="Account.id" :value="Account.id">
                    {{ Account.name }}
                  </a-select-option>
                </a-select>
              </a-form-model-item>
            </a-col>
            <a-col :span="4">
              <a-form-model-item label="実際に受け取った金金金額（円）" :label-col="{ span: 24 }" :wrapper-col="{ span: 24 }">
                <a-input-number v-model="sales_account_item.collection_amount" style="width: 100%;" />
              </a-form-model-item>
            </a-col>
            <a-col :span="4">
              <a-form-model-item label="本伝票未払金金金額（円）" :label-col="{ span: 24 }" :wrapper-col="{ span: 24 }">
                <a-input-number :value="amountOwed" :disabled="true" style="width: 100%;" />
              </a-form-model-item>
            </a-col>
          </a-row>

        </div>

        <!-- <div>
          <a-row gutter="16">
            <a-space>
              <a-button type="primary" @click="handelAddAcount">請求先アカウント新規登録する</a-button>
            </a-space>
          </a-row>
          <div style="margin-top: 16px;">
              <a-table rowKey="id" size="middle" :columns="columnsAccount" :data-source="accountsData"
                :pagination="false">
                <div slot="account" slot-scope="value, item, index">
                  <a-select v-if="!item.isTotal" v-model="item.account" style="width: 100%" @change="(value) => changeAccount(value, item, index)">
                    <a-select-option v-for="Account in accountsItems" :key="Account.id"
                      :value="Account.id">
                      {{ Account.name }}
                    </a-select-option>
                  </a-select>
                </div>
                <div slot="collection_amount" slot-scope="value, item, index">
                  <div v-if="item.isTotal">{{ value }}</div>
                  <a-input-number v-else style="width: 100%"
                    v-model="item.collection_amount"
                    :min="0"
                    :precision="2"></a-input-number>
                </div>
                <div slot="action" slot-scope="value, item, index">
                  <a-button-group v-if="!item.isTotal" size="small">
                    <a-button type="danger" @click="removeAccount(item)">削除</a-button>
                  </a-button-group>
                </div>
              </a-table>
          </div>
        </div> -->
      </a-spin>

      <div style="width: 100%;display: flex;justify-content: center;">
        <div style="margin-top: 32px;">
          <a-popconfirm title="本当に保存しますか??" @confirm="create">
            <a-button type="primary" :loading="loading">保存</a-button>
          </a-popconfirm>
        </div>
      </div>

    </a-card>
    <materials-select-modal v-model="materialsSelectModalVisible" :warehouse="form.warehouse"
      @select="onSelectMaterial"></materials-select-modal>
  </div>
</template>

<script>
import moment from "moment";
import { getSaleOrderNumber } from "@/api/data";
import { saleOrderCreate } from "@/api/sale";
import { userOption, clientsOption, warehousesOption, inventoriesOption, accountsOption } from "@/api/option";
import NP from 'number-precision'

export default {
  components: {
    MaterialsSelectModal: () => import("@/components/MaterialSelectModal/index"),
  },
  data() {
    return {
      description: "新規登録",
      warehouseItems: [],
      handlerItems: [],
      clientsItems: [],
      accountsItems: [],
      materialsSelectModalVisible: false,
      loading: false,
      model: {},
      form: {},
      rules: {
        number: [{ required: true, message: "コードを入力してください", trigger: "change" }],
        warehouse: [{ required: true, message: "入庫を選択してください", trigger: "change" }],
        client: [{ required: true, message: "顧客を選択してください", trigger: "change" }],
        handler: [{ required: true, message: "担当者ーを選択してください", trigger: "change" }],
        handle_time: [{ required: true, message: "処理日を選択してください", trigger: "change" }],
        other_amount: [
          { pattern: new RegExp(/^\d{0,14}(?:\.\d{0,2})?$/), message: "そのその他経費の形式が正しくありません", trigger: "change" },
        ],
      },
      columns: [
        {
          title: "連番",
          dataIndex: "index",
          key: "index",
          width: 45,
          customRender: (value, item, index) => {
            return item.isTotal ? "合計" : index + 1;
          },
        },
        {
          title: "名称",
          dataIndex: "name",
          key: "name",
          width: 150,
        },
        {
          title: "コード",
          dataIndex: "number",
          key: "number",
          width: 150,
        },
        {
          title: "仕様",
          dataIndex: "spec",
          key: "spec",
          width: 150,
        },
        {
          title: "単位",
          dataIndex: "unit",
          key: "unit",
          width: 80,
        },
        {
          title: "販売回数数数量",
          dataIndex: "sales_quantity",
          key: "sales_quantity",
          width: 120,
          scopedSlots: { customRender: "sales_quantity" },
        },
        {
          title: "販売単価（円）",
          dataIndex: "sales_price",
          key: "sales_price",
          width: 120,
          scopedSlots: { customRender: "sales_price" },
        },
        {
          title: "税率",
          dataIndex: "tax",
          key: "tax",
          width: 80,
          scopedSlots: { customRender: "tax" },
        },
        {
          title: "税込金金金額（円）",
          dataIndex: "totalAmount",
          key: "totalAmount",
          width: 200,
          customRender: (value, item) => {
            if (item.isTotal) return value;
            value = NP.times(item.sales_quantity, item.sales_price, ((item.tax / 100 || 0) + 1));
            return item.id ? NP.round(value, 2) : "";
          },
        },
        {
          title: "操作",
          dataIndex: "action",
          key: "action",
          width: 80,
          scopedSlots: { customRender: "action" },
        },
      ],
      materialItems: [],
      columnsAccount: [
        {
          title: "連番",
          dataIndex: "index",
          key: "index",
          width: 45,
          customRender: (value, item, index) => {
            return item.isTotal ? "合計" : index + 1;
          },
        },
        {
          title: "決済口座",
          dataIndex: "account",
          key: "account",
          width: 200,
          scopedSlots: { customRender: "account" },
        },
        {
          title: "支払いい金金金額",
          dataIndex: "collection_amount",
          key: "collection_amount",
          width: 200,
          scopedSlots: { customRender: "collection_amount" },
        },
        {
          title: "操作",
          dataIndex: "action",
          key: "action",
          width: 80,
          scopedSlots: { customRender: "action" },
        },
      ],
      sales_account_items: [],
      sales_account_item: {},
    };
  },
  computed: {
    totalAmount() {
      let totalAmount = 0;
      for (let item of this.materialItems) {
        let amount = NP.times(item.sales_quantity, item.sales_price, ((item.tax / 100 || 0) + 1));
        totalAmount = NP.plus(totalAmount, amount);
      }

      totalAmount = NP.times(totalAmount, this.form.discount || 100, 0.01);
      totalAmount = NP.plus(totalAmount, this.form.other_amount || 0);
      return totalAmount;
    },
    amountOwed() {
      return NP.minus(this.totalAmount, this.sales_account_item.collection_amount || 0);
    },
    goodsData() {
      // データデータ統計合計
      let totalQuantity = 0,
        totalAmount = 0;
      for (let item of this.materialItems) {
        totalQuantity = NP.plus(totalQuantity, item.sales_quantity);
        let amount = NP.times(item.sales_quantity, item.sales_price, ((item.tax / 100 || 0) + 1));
        totalAmount = NP.plus(totalAmount, amount);
      }
      return [
        ...this.materialItems,
        {
          id: "-1",
          isTotal: true,
          name: "",
          sales_quantity: totalQuantity,
          totalAmount: totalAmount,
        },
      ];
    },
    accountsData() {
      // データデータ統計合計
      let totalAmount = 0;
      for (let item of this.sales_account_items) {
        totalAmount = NP.plus(totalAmount, item.collection_amount);
      }
      return [
        ...this.sales_account_items,
        {
          id: "-1",
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
      warehousesOption({ page_size: 999999, is_active: true }).then((data) => {
        this.warehouseItems = data.results;
      });
      userOption({ page_size: 999999, is_active: true }).then((data) => {
        this.handlerItems = data.results;
      });
      clientsOption({ page_size: 999999, is_active: true }).then((data) => {
        this.clientsItems = data.results;
      });
      accountsOption({ page_size: 999999, is_active: true }).then((data) => {
        this.accountsItems = data.results;
      });
    },
    handelAddAcount() {
      this.sales_account_items.push({
        id: this.sales_account_items.length + 1,
        account: "",
        collection_amount: 0,
      });
    },
    removeAccount(item) {
      this.sales_account_items = this.$functions.removeItem(this.sales_account_items, item);
    },
    changeAccount(value, item, idx) {
      let count = this.sales_account_items.filter((_item) => {
        return _item.account == value;
      });
      if (count.length > 1) {
        this.$message.warn("決済口座変更済み!");
        this.sales_account_items[idx].account = "";
      }
    },
    openMaterialModal() {
      if (!this.form.warehouse) {
        this.$message.warn("最初に入庫を選択してください。");
        return false;
      }
      this.materialsSelectModalVisible = true;
    },
    onSelectMaterial(item) {
      let index = this.materialItems.findIndex((_item) => _item.id == item.id);

      if (index != -1) {
        this.$message.warn("商品はすでに存在します");
        return;
      }
      this.materialItems = this.$functions.insertItem(this.materialItems, {
        id: item.id,
        goods: item.goods,
        number: item.goods_number,
        name: item.goods_name,
        spec: item.goods_spec,
        unit: item.unit_name,
        sales_quantity: 1,
        sales_price: item.retail_price,
        totalAmount: 1,
      });

      this.materialItems = [...this.materialItems];
      console.log(this.materialItems);
    },
    removeMaterial(item) {
      this.materialItems = this.$functions.removeItem(this.materialItems, item);
    },
    create() {
      this.$refs.form.validate(async (valid) => {
        if (valid) {
          let ifHasEmptyGoods = false;
          let ifHasEmptyAccounts = false;

          // this.sales_account_items.map((item) => {
          //   if (!item.account || item.collection_amount === "" || item.collection_amount === null) {
          //     ifHasEmptyAccounts = true;
          //   }
          // });
          // if (ifHasEmptyAccounts) {
          //   this.$message.warn("決済口座情報を完全に入力してください");
          //   return false;
          // }

          if (this.materialItems.length == 0) {
            this.$message.warn("商品未登録");
            return false;
          }
          this.materialItems.map((item) => {
            if (item.sales_price === null || !item.sales_quantity) {
              ifHasEmptyGoods = true;
            }
          });
          if (ifHasEmptyGoods) {
            this.$message.warn("販売単価と販売回数数数量は必須です");
            return false;
          }

          let sales_account_items = [];
          if (this.sales_account_item.account && this.sales_account_item.collection_amount > 0) {
            sales_account_items = [this.sales_account_item];
          }

          this.loading = true;
          let formData = {
            ...this.form,
            // sales_account_items: this.sales_account_items.map((item) => {
            //   delete item.id;
            //   return item;
            // }),
            sales_account_items,
            sales_goods_items: this.materialItems.map((item) => {
              return {
                goods: item.goods,
                sales_quantity: item.sales_quantity,
                sales_price: item.sales_price*(1+item.tax/100),
              };
            }),
          };
          formData.total_amount = this.totalAmount;
          saleOrderCreate(formData)
            .then((data) => {
              this.$message.success("作成成功");
              this.$router.push({ path: "/sale/sale_record" });
            })
            .finally(() => {
              this.loading = false;
            });
        }
      });
    },
    resetForm() {
      this.form = { other_amount: 0 };
      this.sales_account_item = { collection_amount: 0 };
      getSaleOrderNumber().then((data) => {
        this.form = { ...this.form, number: data.number, discount: 100 };
      });
      this.materialItems = [];
      this.handelAddAcount();
    },
  },
  mounted() {
    this.initData();
  },
};
</script>
