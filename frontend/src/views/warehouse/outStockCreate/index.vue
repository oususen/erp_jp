<template>
  <div>
    <a-card title="出庫伝票">
      <a-button slot="extra" type="primary" ghost @click="() => { this.$router.go(-1); }"> <a-icon type="left" />戻る</a-button>
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
                <a-form-model-item prop="" :label="info.type === 'purchase' ? '購買返品伝票' : (info.type === 'sales' ? '販売伝票' : '在庫振替伝票')">
                  {{ info.type === 'purchase' ? info.purchase_return_order_number : (info.type === 'sales' ? info.sales_order_number : info.stock_transfer_order_number) }}
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
              <div slot="stock_out_quantity" slot-scope="value, item, index">
                <div v-if="item.isTotal">{{ value }}</div>
                <a-input-number v-else v-model="item.stock_out_quantity" :min="0" size="small"></a-input-number>
              </div>
              <div slot="batch" slot-scope="value, item, index">
                <a-select v-if="!item.isTotal" v-model="item.batch" style="width: 100%">
                  <a-select-option v-for="batch in item.batchItems" :key="batch.id" :value="batch.id">
                    {{ batch.number }}
                  </a-select-option>
                </a-select>
              </div>
              <!-- <div slot="action" slot-scope="value, item, index">
                <a-button-group v-if="!item.isTotal" size="small">
                  <a-button type="danger" @click="removeMaterial(item)">削除</a-button>
                </a-button-group>
              </div> -->
            </a-table>
          </a-form-model>
        </a-spin>
        <div style="display: flex;justify-content: center;width: 100%;">
          <div style="margin-top: 32px;">
          <a-popconfirm title="本当に保存しますか??" @confirm="create">
            <a-button type="primary" :loading="loading">保存</a-button>
          </a-popconfirm>
        </div>
        </div>

      </section>
    </a-card>
  </div>
</template>

<script>
  import { userOption, warehousesOption, batchsOption } from '@/api/option'
  import { stockOutOrderDetail, stockOutCreate } from '@/api/warehouse'
  import NP from 'number-precision'

  export default {
    data() {
      return {
        loading: true,
        info: {},
        form: {},
        rules: {
          handler: [{ required: true, message: '担当者ーを選択してください', trigger: 'change' }],
          handle_time: [{ required: true, message: '処理日を選択してください', trigger: 'change' }]
        },
        warehouseItems: [],
        materialItems: [],
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
            dataIndex: 'goods_name',
            key: 'goods_name',
            width: 150,
          },
          {
            title: 'コード',
            dataIndex: 'goods_number',
            key: 'goods_number',
            width: 150,
          },
          {
            title: '出庫数数数量',
            dataIndex: 'stock_out_quantity',
            key: 'stock_out_quantity',
            width: 120,
            scopedSlots: { customRender: 'stock_out_quantity' },
          },
          {
            title: '出庫予定数数数量',
            dataIndex: 'wait_quantity',
            key: 'wait_quantity',
            width: 120,
          },
          {
            title: '単位',
            dataIndex: 'unit_name',
            key: 'unit_name',
            width: 80,
          },
          {
            title: 'ロット制御',
            dataIndex: 'enable_batch_control',
            key: 'enable_batch_control',
            width: 80,
            customRender: (value, item, index) => {
              return item.isTotal ? '' : (value ? '有効化済み' : '無効')
            },
          },
          {
            title: 'ロット',
            dataIndex: 'batch',
            key: 'batch',
            width: 120,
            scopedSlots: { customRender: 'batch' },
          },
          // {
          //   title: '操作',
          //   dataIndex: 'action',
          //   key: 'action',
          //   width: 80,
          //   scopedSlots: { customRender: 'action' },
          // },
        ],
      }
    },
    created(){
    },
    computed: {
      goodsData() {
        // データデータ統計合計
        let totalQuantity = 0,
          totalAmount = 0;
        for (let item of this.materialItems) {
          totalQuantity = NP.plus(totalQuantity, item.stock_out_quantity);
        }
        return [
          ...this.materialItems,
          {
            id: '-1',
            isTotal: true,
            name: '',
            stock_out_quantity: totalQuantity,
          },
        ];
      },
    },
    methods: {
      async initData() {
        userOption({ page_size: 999999, is_active: true }).then(data => {
          this.handlerItems = data.results;
        });
        stockOutOrderDetail({ id: this.$route.query.id }).then(async data => {
          this.info = data;
          let materialItems = [];
          await Promise.all(data.stock_out_goods_items.map(async (item) => {
            let batchItems = [];
						await batchsOption({
              page_size: 999999,
              goods: item.goods,
              warehouse: data.warehouse
            }).then(data => {
              item.batchItems = data.results;
              item.wait_quantity = item.remain_quantity;
              materialItems.push(item);
            });
					}));
          this.materialItems = materialItems;
        }).finally(() => {
          this.loading = false;
        });
      },
      create() {
        this.$refs.form.validate(async (valid) => {
          if (valid) {
            let ifHasEmptyBatch = false;
            let ifHasEmptyAmount = false;
            this.materialItems.map(item => {
              if (item.enable_batch_control && !item.batch) {
                ifHasEmptyBatch = true;
              }
              if (!item.stock_out_quantity) {
                ifHasEmptyAmount = true;
              }
            })
            if (ifHasEmptyAmount) {
              this.$message.warn('入庫数数数量と出庫数数数量を入力してください');
              return false
            }
            if (ifHasEmptyBatch) {
              this.$message.warn('ロット制御がオンになっている商品は、ロットコードを選択する必要があります');
              return false
            }

            // this.loading = true;
            let formData = {
              ...this.form,
              stock_out_order: this.info.id,
              stock_out_record_goods_items: this.materialItems.map(item => {
                return {
                  stock_out_goods: item.id,
                  stock_out_quantity: item.stock_out_quantity,
                  batch: item.batch
                }
              })
            };
            stockOutCreate(formData).then(data => {
              this.$message.success('作成成功');
              this.$router.push({ path: '/warehouse/outStock' });
            }).finally(() => {
              this.loading = false;
            });
          }
        });
      },
    },
    mounted() {
      this.initData();
    },
  }
</script>
<style>
</style>
