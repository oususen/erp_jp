<template>
  <div>
    <a-row gutter="16">
      <a-col :span="24" :md="8" :xl="6" style="max-width: 256px; margin-bottom: 12px;">
        <a-input-search v-model="searchForm.search" placeholder="伝票コード" allowClear @search="search" />
      </a-col>
      <!-- <a-col :span="24" :md="8" :xl="6" style="max-width: 256px; margin-bottom: 12px;">
        <a-range-picker @change="onChangePicker" />
      </a-col> -->
    </a-row>

    <a-row style="margin-top: 12px;">
      <a-table size="small" :columns="columns" :dataSource="items" rowKey="id" :loading="loading" :pagination="pagination"
        @change="tableChange">
        <div slot="action" slot-scope="value, item">
          <a-button-group size="small">
            <a-button size="small" @click="detial(item)">詳細</a-button>
            <a-popconfirm v-if="item.is_completed" title="本当に無効にしますか??" @confirm="voidItem(item)">
              <a-button type="danger" :disabled="item.is_void">{{ item.is_void ? '無効済み' : '無効'}}</a-button>
            </a-popconfirm>
          </a-button-group>
        </div>
      </a-table>
    </a-row>
  </div>
</template>

<script>
  import { stockOutRecordsList, stockOutOrdersVoid } from '@/api/warehouse'

  export default {
    name: 'SaleRecord',
    components: {
    },
    data() {
      return {
        columns: [
          {
            title: '連番',
            dataIndex: 'index',
            key: 'index',
            customRender: (value, item, index) => {
              return index + 1
            },
            width: 45
          },
          {
            title: '伝票コード',
            dataIndex: 'stock_out_order_number',
            sorter: true,
          },
          {
            title: '入庫',
            dataIndex: 'warehouse_name',
          },
          {
            title: '担当者',
            dataIndex: 'handler_name',
          },
          {
            title: '処理日',
            dataIndex: 'handle_time',
            width: 170
          },
          {
            title: '操作',
            dataIndex: 'action',
            scopedSlots: { customRender: 'action' },
            width: 147
          },
        ],
        searchForm: { page: 1, is_completed: false, page_size: 16 },
        pagination: { current: 1, total: 0, pageSize: 16 },
        loading: false,
        items: [],
        visible: false,
        targetItem: {},
        form: {},
      };
    },
    computed: {
    },
    methods: {
      initialize() {
        this.list();
      },
      list() {
        this.loading = true;
        stockOutRecordsList(this.searchForm).then(data => {
          this.pagination.total = data.count;
          this.items = data.results;
        }).finally(() => {
          this.loading = false;
        });
      },
      tableChange(pagination, filters, sorter) {
        this.searchForm.page = pagination.current;
        this.pagination.current = pagination.current;
        this.searchForm.ordering = `${sorter.order == 'descend' ? '-' : ''}${sorter.field}`;
        this.list();
      },
      onChangePicker(date, dateString) {
        let startDate = date[0], endDate = date[1];
        this.searchForm.start_date = startDate ? startDate.format('YYYY-MM-DD') : undefined;
        this.searchForm.end_date = endDate ? endDate.add(1, 'days').format('YYYY-MM-DD') : undefined;
        this.search();
      },
      search() {
        this.searchForm.page = 1;
        this.pagination.current = 1;
        this.list();
      },
      toStockIn(item) {
        this.$router.push({ path: '/warehouse/outStock_create', query: { id: item.id } });
      },
      detial(item) {
        this.$router.push({ path: '/warehouse/outStock_record_detail', query: { id: item.id } });
      },
      voidItem(item) {
        stockOutOrdersVoid({ id: item.id }).then(() => {
          this.$message.success('無効化成功');
          this.list();
        });
      },
    },
    mounted() {
      this.initialize();
    },
  }
</script>