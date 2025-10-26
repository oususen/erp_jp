<template>
  <div>
    <a-modal v-model="visible" width="750px" :confirmLoading="loading" :maskClosable="false" @cancel="cancel" @ok="confirm">
      <div slot="title">{{form.id ? '商品情報を編集する' : '商品情報を追加' }}</div>
      <div>
        <a-form-model
            ref="form"
            :model="form"
            :rules="rules"
            :label-col="{ span: 4, md: 8 }"
            :wrapper-col="{ span: 20, md: 16 }">
          <a-row :gutter="12">
            <a-divider orientation="left" id="basic-information">
              基本情報
            </a-divider>
            <a-col :span="24" :md="12">
              <a-form-model-item prop="barcode" label="バーコード">
                <a-input v-model="form.barcode" />
                <!-- <a-input-search v-model="form.barcode">
                  <a-button slot="enterButton" type="primary" @click.native="getCode">バーコード生成</a-button>
                </a-input-search> -->
              </a-form-model-item>
            </a-col>
            <a-col :span="24" :md="12">
              <a-form-model-item prop="number" label="商品コード">
                <a-input v-model="form.number" />
              </a-form-model-item>
            </a-col>
            <a-col :span="24" :md="12">
              <a-form-model-item prop="name" label="商品名">
                <a-input v-model="form.name" />
              </a-form-model-item>
            </a-col>
            <a-col :span="24" :md="12">
              <a-form-model-item prop="category" label="カテゴリ">
                <a-select v-model.number="form.category" style="width: 100%" :allowClear="true">
                  <a-select-option
                      v-for="item of classificationItems"
                      :key="item.id"
                      :value="item.id">{{ item.name }}
                  </a-select-option>
                </a-select>
                <!-- <a-button
                  type="primary"
                  style="width: 20%; margin-left: 5%"
                  @click="
                    resetForm();
                    categoryVisible = true;">
                  <a-icon type="plus" />
                </a-button> -->
              </a-form-model-item>
            </a-col>
            <!-- <a-col :span="24" :md="12">
              <a-form-model-item prop="unit" label="単位">
                <a-select v-model.number="form.unit" :allowClear="true">
                  <a-select-option
                      v-for="item of unitItems"
                      :key="item.id"
                      :value="item.id">{{ item.name }}
                  </a-select-option>
                </a-select>
              </a-form-model-item>
            </a-col> -->
            <a-col :span="24" :md="12">
              <a-form-model-item prop="spec" label="仕様">
                <a-input v-model="form.spec" />
              </a-form-model-item>
            </a-col>
            <!-- <a-col :span="24" :md="12">
              <a-form-model-item prop="enable_shelf_life" label="保存期間を有効化">
                <a-switch
                  checked-children="有効化"
                  un-checked-children="無効化"
                  v-model="form.enable_shelf_life"/>
              </a-form-model-item>
            </a-col> -->
            <a-col :span="24" :md="12">
              <a-form-model-item prop="shelf_life_days" label="品質保証期間日数">
                <a-input v-model="form.shelf_life_days" suffix="日" />
              </a-form-model-item>
            </a-col>
            <a-col :span="24" :md="12">
              <a-form-model-item
                  prop="shelf_life_warning_days"
                  label="期限切れ間近警告日">
                <a-input v-model="form.shelf_life_warning_days" suffix="日" />
              </a-form-model-item>
            </a-col>
            <a-col :span="24" :md="12">
              <a-form-model-item prop="enable_batch_control" label="ロット制御を有効化">
                <a-switch
                    checked-children="有効化"
                    un-checked-children="無効化"
                    v-model="form.enable_batch_control"
                />
              </a-form-model-item>
            </a-col>
            <a-col :span="24" :md="12">
              <a-form-model-item prop="is_active" label="状態">
                <a-select v-model="form.is_active" style="width: 100%;">
                  <a-select-option :value="1">有効化</a-select-option>
                  <a-select-option :value="0">凍結</a-select-option>
                </a-select>
              </a-form-model-item>
            </a-col>
            <a-col :span="24" :md="12">
              <a-form-model-item prop="remark" label="単位">
                <a-input v-model="form.remark" allowClear />
              </a-form-model-item>
            </a-col>
          </a-row>
          <a-row :gutter="12">
            <a-divider orientation="left" id="price-management">
              価格管理
            </a-divider>
            <a-col :span="24" :md="12">
              <a-form-model-item prop="purchase_price" label="購買価格（円）">
                <a-input-number v-model="form.purchase_price" style="width: 100%"/>
              </a-form-model-item>
            </a-col>
            <a-col :span="24" :md="12">
              <a-form-model-item prop="retail_price" label="小売価格（円）">
                <a-input-number v-model="form.retail_price" style="width: 100%" />
              </a-form-model-item>
            </a-col>
            <a-col :span="24" :md="12">
              <a-form-model-item prop="level_price1" label="等級価格1（円）">
                <a-input-number v-model="form.level_price1" style="width: 100%" />
              </a-form-model-item>
            </a-col>
            <a-col :span="24" :md="12">
              <a-form-model-item prop="level_price2" label="等級価格2（円）">
                <a-input-number v-model="form.level_price2" style="width: 100%" />
              </a-form-model-item>
            </a-col>
            <a-col :span="24" :md="12">
              <a-form-model-item prop="level_price3" label="等級価格3（円）">
                <a-input-number v-model="form.level_price3" style="width: 100%" />
              </a-form-model-item>
            </a-col>
          </a-row>
          <a-row :gutter="12">
            <a-divider orientation="left" id="graphic-information">
              図面情報
            </a-divider>
            <a-col :span="24" :md="24">
              <a-upload
                  :action="actionUrl"
                  list-type="picture-card"
                  :headers="{ 'Authorization':'Bearer '+ Cookies.get('access')   }"
                  :file-list="form.image_items"
                  @preview="handlePreview"
                  @change="handleChange"
                  :before-upload="beforeUpload"
                  name="file">
                <div>
                  <a-icon type="plus" />
                  <div class="ant-upload-text"></div>
                </div>
              </a-upload>
              <a-modal
                  :visible="previewVisible"
                  :footer="null"
                  @cancel="handleCancel"
              >
                <img alt="example" style="width: 100%" :src="previewImage" />
              </a-modal>
            </a-col>
            <a-col :span="24" :md="24">
              <a-textarea
                  placeholder="商品詳細"
                  :rows="4"
                  v-model="form.description"
              />
            </a-col>
          </a-row>
          <a-row :gutter="12">
            <a-divider orientation="left" id="beginning-inventory">
              期首在庫
            </a-divider>
            <a-col :span="24" :md="24">
              <a-table
                  rowkey="columns"
                  :columns="columns"
                  :data-source="warehouseItems"
                  :loading="loading"
                  :pagination="false"
                  style="width: 100%" >
                <div slot="initial_quantity" slot-scope="value, item">
                  <div v-if="!!form.enable_batch_control">
                    <a-input :value="item.initial_quantity" disabled style="width:75%;" />
                    <a-button @click="chooseBatch(item)">ロット</a-button>
                  </div>
                  <a-input-number v-else
                                  :value="item.initial_quantity"
                                  :min="0"
                                  @change="(value) => changeQuantity(value, item)" />
                </div>
              </a-table>
            </a-col>
          </a-row>
          <a-row :gutter="12">
            <a-divider orientation="left" id="inventory-warning">
              在庫アラート
            </a-divider>
            <a-col :span="24" :md="12">
              <a-form-model-item prop="enable_inventory_warning" label="在庫警告を有効化">
                <a-switch
                    checked-children="有効化"
                    un-checked-children="無効化"
                    v-model="form.enable_inventory_warning"/>
              </a-form-model-item>
            </a-col>
            <a-col :span="24" :md="12" v-if="!!form.enable_inventory_warning">
              <a-form-model-item prop="inventory_upper" label="在庫上限">
                <a-input-number v-model="form.inventory_upper" style="width: 100%" />
              </a-form-model-item>
            </a-col>
            <a-col :span="24" :md="12" v-if="!!form.enable_inventory_warning">
              <a-form-model-item prop="inventory_lower" label="在庫下限">
                <a-input-number v-model="form.inventory_lower" style="width: 100%" />
              </a-form-model-item>
            </a-col>
            <!-- <a-col :span="24" :md="12">
              <a-form-model-item
                prop="inventory_warning_upper_limit"
                label="在庫警告上限">
                <a-input-number
                  v-model="form.inventory_warning_upper_limit"
                  style="width: 100%" />
              </a-form-model-item>
            </a-col>
            <a-col :span="24" :md="12">
              <a-form-model-item
                prop="inventory_warning_lower_limit"
                label="在庫警告下限">
                <a-input-number
                  v-model="form.inventory_warning_lower_limit"
                  style="width: 100%"/>
              </a-form-model-item>
            </a-col> -->
          </a-row>
        </a-form-model>
      </div>
      <!-- ロット -->
      <a-modal
          :title="batchTitle"
          v-model="batchVisible"
          width="750px"
          cancelText="閉じる"
          :maskClosable="false"
          @cancel="batchVisible=false"
          @ok="confirmChoosed">
        <div style="margin-bottom: 16px">
          <a-button type="primary" icon="plus" style="margin: 0 8px;" @click="addLine">追加</a-button>
        </div>
        <a-table
            rowkey="columnsBatch"
            :columns="columnsBatch"
            :data-source="batchItems"
            :pagination="false"
            style="width: 100%" >
          <div slot="initial_quantity" slot-scope="value, item">
            <a-input-number
                :value="item.initial_quantity"
                :min="0"
                @change="(value) => changeQuantityBatch(value, item, 'initial_quantity')" />
          </div>
          <div slot="number" slot-scope="value, item">
            <a-input
                :value="item.number"
                @change="(e) => changeQuantityBatch(e, item, 'number')" />
          </div>
          <div slot="production_date" slot-scope="value, item">
            <a-date-picker
                :value="item.production_date"
                valueFormat="YYYY-MM-DD"
                @change="(value) => changeQuantityBatch(value, item, 'production_date')" />
          </div>
          <div slot="action" slot-scope="value,item">
            <a-button icon=":minus" @click="removeLine(item)"></a-button>
          </div>
        </a-table>
      </a-modal>

    </a-modal>
  </div>
</template>

<script>
import Cookies from 'js-cookie'
import { goodsInformationCreate, goodsInformationUpdate } from '@/api/goods'
import config from "@/utils/config"
function getBase64(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = () => resolve(reader.result);
    reader.onerror = (error) => reject(error);
  });
}
export default {
  name: 'FormModal',
  props: ['visible', 'form', 'warehouseItems', 'classificationItems', 'unitItems'],
  model: { prop: 'visible', event: 'cancel' },
  data() {
    return {
      Cookies,
      actionUrl:config.baseURL+'goods_images/',
      batchTitle: 'ロットを管理する',
      batchVisible: false,
      loading: false,
      columns: [
        {
          title: "入庫",
          dataIndex: "name",
          key: "name",
        },
        {
          title: "初期在庫",
          dataIndex: "initial_quantity",
          key: "initial_quantity",
          scopedSlots: { customRender: "initial_quantity" },
        },
      ],
      isKeepAdd: false,
      categoryForm: {},
      categoryVisible: false,
      rules: {
        name: [
          { required: true, message: "商品名を入力してください", trigger: "change" },
        ],
        number: [
          { required: true, message: "商品コードを入力してください", trigger: "change" },
        ],
      },
      previewVisible: false,
      previewImage: "",
      columnsBatch: [
        {
          title: '連番',
          dataIndex: 'index',
          key: 'index',
          customRender: (value, item, index) => {
            return index + 1
          },
        },
        {
          title: "コード",
          dataIndex: "number",
          key: "number",
          scopedSlots: { customRender: "number" },
        },
        {
          title: "初期在庫",
          dataIndex: "initial_quantity",
          key: "initial_quantity",
          scopedSlots: { customRender: "initial_quantity" },
        },
        {
          title: "製造日",
          dataIndex: "production_date",
          key: "production_date",
          scopedSlots: { customRender: "production_date" },
        },
        {
          title: '操作',
          dataIndex: 'action',
          scopedSlots: { customRender: 'action' },
          width: '80px'
        },
      ],
      curWarehouse: {},
      batchItems: []
    };
  },
  methods: {
    chooseBatch(item) {
      this.batchTitle = 'ロットを管理する-' + item.name;
      this.curWarehouse = item;
      if (item.batch_items) {
        this.batchItems = item.batch_items;
      } else {
        this.batchItems = [
          {
            key: 'uni1',
            number: '',
            initial_quantity: 1,
            production_date: null,
          }
        ];
      }
      this.batchVisible = true;
    },
    confirmChoosed() {
      let ifHasEmpty = false;
      let sumAmount = 0;
      this.batchItems.map(item => {
        sumAmount+=item.initial_quantity
        if (!item.number || !item.initial_quantity || !item.production_date) {
          ifHasEmpty = true;
        }
      })
      if (ifHasEmpty) {
        this.$message.warn('ロット情報を完全に入力してください!');
        return
      }
      let tmp = {...this.curWarehouse, ...{ batch_items: this.batchItems, initial_quantity: sumAmount }}
      this.warehouseItems = this.$functions.replaceItem(this.warehouseItems, tmp);
      this.batchVisible = false;
    },
    addLine() {
      const { batchItems } = this;
      const newData = {
        key: 'uni' + batchItems.length + 1,
        number: '',
        initial_quantity: 1,
        production_date: null,
      };
      this.batchItems = [...batchItems, newData];
    },
    removeLine(item) {
      this.batchItems = this.$functions.removeItemBatch(this.batchItems, item);
    },
    changeQuantity(value, item) {
      item['initial_quantity'] = value || 0;
      this.warehouseItems = this.$functions.replaceItem(this.warehouseItems, item);
    },
    changeQuantityBatch(e, item, pro) {
      if (pro === 'number') {
        item[pro] = e.target.value;
      } else {
        item[pro] = e;
      }
      this.batchItems[item.key - 1] = item;
    },
    async handlePreview(file) {
      if (!file.url && !file.preview) {
        file.preview = await getBase64(file.originFileObj);
      }
      this.previewImage = file.url || file.preview;
      this.previewVisible = true;
    },
    handleChange({ fileList }) {
      this.$set(this.form,'image_items',fileList);
    },
    beforeUpload() {},
    handleCancel() {
      this.previewVisible = false;
    },
    confirm() {
      let image_items = this.form.image_items.map(item => { return item.response.id })
      let inventory_items = this.warehouseItems.map(item => {
        return {
          warehouse: item.id,
          initial_quantity: item.initial_quantity,
          batch_items: this.form.enable_batch_control ? item.batch_items : []
        }
      })
      let formatData = {
        ...this.form,
        ...{
          goods_images: image_items,
          inventory_items
        }
      }
      console.log(formatData)
      this.$refs.form.validate(valid => {
        if (valid) {
          this.loading = true;
          let func = this.form.id ? goodsInformationUpdate : goodsInformationCreate;
          func(formatData).then(data => {
            this.$message.success(this.form.id ? '更新成功' : '新規登録成功');
            this.$emit(this.form.id ? 'update' : 'create', data);
            this.cancel();
          }).finally(() => {
            this.loading = false;
          });
        }
      });
    },
    cancel() {
      this.$emit('cancel', false);
      this.$refs.form.resetFields();
    },
  },
  watch: {
    // 'form.image_items': {
    //   handler(newVal) {
    //     if (Array.isArray(newVal)) {
    //       var images = newVal.map((file)=>{
    //         if (file.status) {
    //           if (file.status == 'done') {
    //             if (file.response && file.response.id) {
    //               return file.response.id;
    //             }
    //             if (file.uid) {
    //             return file.uid;
    //           }
    //           }
    //         }
    //       });
    //       this.$set(this.form,'images',images);
    //     }
    //   },
    //   deep: true
    // },
  }
}
</script>

<style scoped>
</style>