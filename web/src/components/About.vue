<template>
  <el-dialog
    title="制作人员"
    :visible.sync="visible"
    :width="isMobile ? '90%' : '50%'"
    :show-close="false"
    :before-close="Close"
  >
    <div class="author-content">
      <div class="author-links">
        <el-button
          type="primary"
          size="small"
          @click="
            openLink(
              'https://www.bilibili.com/video/BV1XmLFz5E7Y/?spm_id_from=333.1387.homepage.video_card.click'
            )
          "
        >
          视频链接
        </el-button>
        <el-button
          type="info"
          size="small"
          @click="openLink('https://space.bilibili.com/38187048')"
        >
          作者空间
        </el-button>
        <el-button
          type="success"
          size="small"
          @click="openLink('https://github.com/QuantAskk/pokemonle')"
        >
          项目源地址
        </el-button>
      </div>
      <div class="author-cards">
        <el-card :body-style="{ padding: '0px' }" class="author-card">
          <img src="@/assets/img/QAHead.jpg" class="author-avatar" />
          <div class="author-info">
            <span>QuantAsk</span>
            <br />
            <el-tag size="mini" type="info">作者</el-tag>
          </div>
        </el-card>
        <el-card :body-style="{ padding: '0px' }" class="author-card">
          <img src="@/assets/img/GengerHead.jpg" class="author-avatar" />
          <div class="author-info">
            <span>流明Luminous</span>
            <br />
            <el-tag size="mini" type="info">UI优化</el-tag>
          </div>
        </el-card>
      </div>
    </div>

    <span slot="footer" class="dialog-footer">
      <el-button type="primary" @click="Close">确 定</el-button>
    </span>
  </el-dialog>
</template>
<script>
export default {
  name: "About",
  props: {
    visible: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      isMobile: window.innerWidth <= 768,
    };
  },
  methods: {
    Close() {
      this.$emit("update:visible", false);
    },
  },
};
</script>
