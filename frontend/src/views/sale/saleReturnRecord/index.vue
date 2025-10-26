<template>
  <div>
    <a-card title="販売返品記録">
      <a-row gutter="16">
        <a-col :span="24" :md="8" :xl="6" style="max-width: 256px; margin-bottom: 12px;">
          <a-input-search v-model="searchForm.search" placeholder="伝票コード,仕入先コード/名称" allowClear @search="search" />
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
            </a-button-group>
          </div>
        </a-table>
      </a-row>
    </a-card>
  </div>
</template>

<script>
  import { saleReturnOrderList } from '@/api/sale'

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
            title: '戻りコード',
            dataIndex: 'number',
            sorter: true,
          },
          {
            title: '販売伝票コード',
            dataIndex: 'sales_order',
          },
          {
            title: '顧客',
            dataIndex: 'client_name',
          },
          {
            title: '担当者',
            dataIndex: 'handler_name',
          },
          {
            title: '処理日',
            dataIndex: 'handle_time',
            width: 150
          },
          {
            title: '返品された合計数数数量',
            dataIndex: 'total_quantity',
            width: 120
          },
          {
            title: '返品総金金金額',
            dataIndex: 'total_amount',
            width: 120
          },
          {
            title: '支払いい金金金額',
            dataIndex: 'payment_amount',
            width: 120
          },
          {
            title: 'そのその他費用',
            dataIndex: 'other_amount',
            width: 120
          },
          {
            title: '操作',
            dataIndex: 'action',
            scopedSlots: { customRender: 'action' },
            width: 200
          },
        ],
        searchForm: { page: 1, page_size: 16 },
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
        saleReturnOrderList(this.searchForm).then(data => {
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
      detial(item) {
        this.$router.push({ path: '/sale/sale_return_detail', query: { id: item.id } });
      },
    },
    mounted() {
      this.initialize();
    },
  }
</script>