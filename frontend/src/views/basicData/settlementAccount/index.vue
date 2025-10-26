<template>
  <div>
    <a-card title="決済口座">
      <a-row gutter="16">
        <a-col :span="24" style="max-width: 200px; margin-bottom: 12px;">
          <a-select v-model="searchForm.is_active" placeholder="状態" allowClear style="width: 100%;" @change="search">
            <a-select-option :value="true">有効化</a-select-option>
            <a-select-option :value="false">凍結</a-select-option>
          </a-select>
        </a-col>
        <a-col :span="24" style="max-width: 200px; margin-bottom: 12px;">
          <a-input v-model="searchForm.search" placeholder="コード, 名称, 備考" allowClear @pressEnter="search" />
        </a-col>
        <a-col :span="24" style="width: 100px; margin-bottom: 12px;">
          <a-button type="primary" icon="search" @click="search">検索</a-button>
        </a-col>

        <a-col :span="24" style="width: 300px; margin-bottom: 12px;">
          <a-button-group>
            <a-button icon="file-excel" @click="downloadTemplate">テンプレートダウンロード</a-button>
            <a-upload name="file" :showUploadList="false" :customRequest="importExcel">
              <a-button icon="upload">インポート</a-button>
            </a-upload>
            <a-button icon="download" @click="exportExcel">エクスポート</a-button>
          </a-button-group>
        </a-col>

        <div style="margin-bottom: 12px; float: right;">
          <a-button type="primary" icon="plus" style="margin: 0 8px;" @click="openFormModal(form)">決済口座新規登録</a-button>
        </div>
      </a-row>

      <a-row style="margin-top: 12px;">
        <a-table size="small" :columns="columns" :dataSource="items" rowKey="id" :loading="loading" :pagination="pagination"
          @change="tableChange">
          <div slot="is_active" slot-scope="value">
            <a-tag :color="value ? 'green' : 'red'">{{value ? '有効化' : '凍結'}}</a-tag>
          </div>
          <div slot="action" slot-scope="value, item">
            <a-button-group>
              <a-button icon="edit" size="small" @click="openFormModal(item)">編集</a-button>
              <a-popconfirm title="本当に削除しますか?" @confirm="destroy(item.id)">
                <a-button type="danger" icon="delete" size="small">削除</a-button>
              </a-popconfirm>
            </a-button-group>
          </div>
        </a-table>
      </a-row>
    </a-card>
    <form-modal v-model="visible" :form="targetItem" @create="create" @update="update" />
    <a-modal v-model="importLoading" :footer="null" :maskClosable="false" :closable="false">
      <div>
        <a-spin style="margin-right: 12px;" />インポート中, お待ちください...
      </div>
    </a-modal>
  </div>
</template>

<script>
  import { exportExcel } from '@/utils/excel'
  import { settlementAccountExport } from '@/api/export'
  import { settlementAccountTemplate, settlementAccountImport } from '@/api/import'
  import { settlementAccountList, settlementAccountDestroy } from '@/api/basicData'
  import { getSettlementAccountNumber } from '@/api/data'

  export default {
    name: 'Warehouse',
    components: {
      FormModal: () => import('./FormModal.vue'),
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
          },
          {
            title: '口座コード',
            dataIndex: 'number',
          },
          {
            title: '口座名',
            dataIndex: 'name',
            sorter: true,
          },
          {
            title: '口座タイプ',
            dataIndex: 'type_display',
          },
          {
            title: '状態',
            dataIndex: 'is_active',
            scopedSlots: { customRender: 'is_active' }
          },
          {
            title: '口座残高（円）',
            dataIndex: 'balance_amount',
          },
          {
            title: '操作',
            dataIndex: 'action',
            scopedSlots: { customRender: 'action' },
            width: '156px'
          },
        ],
        searchForm: { search: '', page: 1, page_size: 16 },
        pagination: { current: 1, total: 0, pageSize: 16 },
        loading: false,
        items: [],

        visible: false,
        targetItem: {},
        form: { is_active: true },
        importLoading: false,
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
        settlementAccountList(this.searchForm).then(data => {
          this.pagination.total = data.count;
          this.items = data.results;
        }).finally(() => {
          this.loading = false;
        });
      },
      create(item) {
        // this.items.splice(0, 0, item);
        this.list();
      },
      update(item) {
        this.items.splice(this.items.findIndex(i => i.id == item.id), 1, item);
      },
      search() {
        this.searchForm.page = 1;
        this.pagination.current = 1;
        this.list();
      },
      openFormModal(item) {
        if (!item.id) {
          getSettlementAccountNumber().then(data => {
            this.targetItem = { ...item, ...{ number: data.number } };
          })
        } else {
          this.targetItem = { ...item };
        }
        this.visible = true;
      },
      destroy(id) {
        settlementAccountDestroy({ id }).then(() => {
          // this.items.splice(this.items.findIndex(item => item.id == id), 1);
          this.$message.success('削除成功');
          this.list();
        });
      },
      exportExcel() {
        settlementAccountExport(this.searchForm).then(resp => {
          exportExcel(resp.data, '決済口座一覧');
        }).catch(err => {
          this.$message.error(err.response.data.error);
        });
      },
      downloadTemplate () {
        settlementAccountTemplate().then(resp => {
          exportExcel(resp.data, '決済口座インポートテンプレート');
        }).catch(err => {
          this.$message.error(err.response.data.error);
        });
      },
      importExcel(item) {
        let data = new FormData();
        data.append('file', item.file);
        this.importLoading = true;
        setTimeout(() => {
          settlementAccountImport(data)
            .then(() => {
              this.$message.success('インポート成功');
              this.list();
            })
            .catch(err => {
              this.$message.error(err.response.data.detail);
            })
            .finally(() => {
              this.importLoading = false;
            });
        }, 1000);
      },
      tableChange(pagination, filters, sorter) {
        this.searchForm.page = pagination.current;
        this.pagination.current = pagination.current;
        this.searchForm.ordering = `${sorter.order == 'descend' ? '-' : ''}${sorter.field}`;
        this.list();
      },
    },
    mounted() {
      this.initialize();
    },
  }
</script>