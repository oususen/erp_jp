<template>
  <div>
    <a-card title="入庫受領書">
      <a-button
        slot="extra"
        type="primary"
        ghost
        @click="
          () => {
            this.$router.go(-1);
          }
        "
      >
        <a-icon type="left" />戻る</a-button
      >
      <section>
        <a-spin :spinning="loading">
          <a-form-model ref="form" :model="form" :rules="rules" :label-col="{ span: 7 }" :wrapper-col="{ span: 16 }">
            <a-row>
              <a-col :span="6" style="width: 320px;">
                <a-form-model-item prop="number" label="コード">
                  {{ info.number }}
                </a-form-model-item>
              </a-col>
              <a-col :span="6" style="width: 320px;">
                <a-form-model-item prop="warehouse_name" label="入庫">
                  {{ info.warehouse_name }}
                </a-form-model-item>
              </a-col>
              <a-col :span="6" style="width: 320px;">
                <a-form-model-item prop="type_display" label="入庫タイプ">
                  {{ info.type_display }}
                </a-form-model-item>
              </a-col>
              <a-col :span="6" style="width: 320px;">
                <a-form-model-item
                  prop=""
                  :label="
                    info.type === 'purchase' ? '購買伝票' : info.type === 'sales_return' ? '販売返品伝票' : '在庫振替伝票'
                  "
                >
                  {{
                    info.type === "purchase"
                      ? info.purchase_order_number
                      : info.type === "sales_return"
                      ? info.sales_return_order_number
                      : info.stock_transfer_order_number
                  }}
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
            <a-table rowKey="id" size="middle" :columns="columns" :data-source="goodsData" :pagination="false">
              <div slot="stock_in_quantity" slot-scope="value, item, index">
                <div v-if="item.isTotal">{{ value }}</div>
                <a-input-number v-else v-model="item.stock_in_quantity" :min="0" size="small"></a-input-number>
              </div>
              <div slot="batch_number" slot-scope="value, item, index">
                <a-input v-if="!item.isTotal" v-model="item.batch_number" size="small"></a-input>
              </div>
              <div slot="production_date" slot-scope="value, item, index">
                <a-date-picker
                  v-if="!item.isTotal"
                  v-model="item.production_date"
                  valueFormat="YYYY-MM-DD"
                  style="width: 100%"
                />
              </div>
              <!-- <div slot="action" slot-scope="value, item, index">
                <a-button-group v-if="!item.isTotal" size="small">
                  <a-button type="danger" @click="removeMaterial(item)">削除</a-button>
                </a-button-group>
              </div> -->
            </a-table>
          </a-form-model>
        </a-spin>
        <div style="width: 100%;display: flex;justify-content: center;">
          <div style="display: flex;justify-content: center;width: 100%;">
          <div style="margin-top: 32px;">
          <a-popconfirm title="本当に保存しますか??" @confirm="create">
            <a-button type="primary" :loading="loading">保存</a-button>
          </a-popconfirm>
        </div>
        </div>

        </div>

      </section>
    </a-card>
  </div>
</template>

<script>
import { userOption, warehousesOption } from "@/api/option";
import { stockInOrderDetail, stockInCreate } from "@/api/warehouse";
import NP from "number-precision";

export default {
  data() {
    return {
      loading: true,
      info: {},
      form: {},
      rules: {
        // name: [{ required: true, message: '名称を入力してください', trigger: 'change' }],
        // number: [{ required: true, message: 'コードを入力してください', trigger: 'change' }],
        // initial_arrears_amount: [
        //   { pattern: new RegExp(/^\d{0,14}(?:\.\d{0,2})?$/), message: '初期未払金金金額の形式が不正です', trigger: 'change' }
        // ],
        handler: [{ required: true, message: "担当者ーを選択してください", trigger: "change" }],
        handle_time: [{ required: true, message: "処理日を選択してください", trigger: "change" }],
      },
      warehouseItems: [],
      handlerItems: [],
      materialItems: [],
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
          dataIndex: "goods_name",
          key: "goods_name",
          width: 150,
        },
        {
          title: "コード",
          dataIndex: "goods_number",
          key: "goods_number",
          width: 150,
        },
        {
          title: "入庫数数数量",
          dataIndex: "stock_in_quantity",
          key: "stock_in_quantity",
          width: 120,
          scopedSlots: { customRender: "stock_in_quantity" },
        },
        {
          title: "入庫予定数数数量",
          dataIndex: "remain_quantity",
          key: "remain_quantity",
          width: 120,
        },
        {
          title: "単位",
          dataIndex: "unit_name",
          key: "unit_name",
          width: 80,
        },
        {
          title: "ロット制御",
          dataIndex: "enable_batch_control",
          key: "enable_batch_control",
          width: 80,
          customRender: (value, item, index) => {
            return item.isTotal ? "" : value ? "有効化済み" : "無効";
          },
        },
        {
          title: "ロット",
          dataIndex: "batch_number",
          key: "batch_number",
          width: 120,
          scopedSlots: { customRender: "batch_number" },
        },
        {
          title: "製造日",
          dataIndex: "production_date",
          key: "production_date",
          width: 150,
          scopedSlots: { customRender: "production_date" },
        },
        {
          title: "品質保証期間日数",
          dataIndex: "shelf_life_days",
          key: "shelf_life_days",
          width: 120,
        },
        // {
        //   title: '操作',
        //   dataIndex: 'action',
        //   key: 'action',
        //   width: 80,
        //   scopedSlots: { customRender: 'action' },
        // },
      ],
    };
  },
  created() {
    this.initData();
  },
  computed: {
    goodsData() {
      // データデータ統計合計
      let totalQuantity = 0,
        totalAmount = 0;
      for (let item of this.materialItems) {
        totalQuantity = NP.plus(totalQuantity, item.stock_in_quantity);
      }
      return [
        ...this.materialItems,
        {
          id: "-1",
          isTotal: true,
          name: "",
          stock_in_quantity: totalQuantity,
        },
      ];
    },
  },
  methods: {
    initData() {
      warehousesOption({ page_size: 999999, is_active: true }).then((data) => {
        this.warehouseItems = data.results;
      });
      userOption({ page_size: 999999, is_active: true }).then((data) => {
        this.handlerItems = data.results;
      });
      stockInOrderDetail({ id: this.$route.query.id })
        .then((data) => {
          this.info = data;
          this.materialItems = data.stock_in_goods_items;
        }) 
        .finally(() => {
          this.loading = false;
        });
    },
    create() {
      this.$refs.form.validate(async (valid) => {
        if (valid) {
          let ifHasEmptyBatch = false;
          let ifHasEmptyAmount = false;
          this.materialItems.map((item) => {
            if (item.enable_batch_control && !item.batch_number) {
              ifHasEmptyBatch = true;
            }
            if (!item.stock_in_quantity) {
              ifHasEmptyAmount = true;
            }
          });
          if (ifHasEmptyAmount) {
            this.$message.warn("入庫数数数量を入力してください");
            return false;
          }
          if (ifHasEmptyBatch) {
            this.$message.warn("ロット制御がオンになっている商品は、ロットコードを入力する必要があります");
            return false;
          }

          // this.loading = true;
          let formData = {
            ...this.form,
            stock_in_order: this.info.id,
            stock_in_record_goods_items: this.materialItems.map((item) => {
              return {
                stock_in_goods: item.id,
                stock_in_quantity: item.stock_in_quantity,
                batch_number: item.batch_number,
                production_date: item.production_date,
              };
            }),
          };
          stockInCreate(formData)
            .then((data) => {
              this.$message.success("作成成功");
              this.$router.push({ path: "/warehouse/inStock" });
            })
            .finally(() => {
              this.loading = false;
            });
        }
      });
    },
  },
  mounted() {
    this.initData();
  },
};
</script>
<style></style>
