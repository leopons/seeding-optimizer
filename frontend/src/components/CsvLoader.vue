<template>
  <div
    class="csv-upload"
    @dragover.prevent
    @drop="handleFileUpload"
    @click="$refs.fileInput.click()"
  >
    <input
      type="file"
      ref="fileInput"
      @change="handleFileUpload"
      style="display: none"
    />
    <div class="csv-upload__label">{{ text }}</div>
  </div>
</template>

<script>
export default {
  name: "CsvLoader",
  props: {
    handleData: Function,
    text: String,
  },
  methods: {
    handleFileUpload(event) {
      event.preventDefault();
      const file = event.dataTransfer
        ? event.dataTransfer.files[0]
        : event.target.files[0];
      const reader = new FileReader();
      reader.readAsText(file);
      reader.onload = () => {
        const csvData = reader.result;
        const rows = csvData.split("\n");
        const headers = rows[0].split(",");
        const data = [];
        for (let i = 1; i < rows.length; i++) {
          const values = rows[i].split(",");
          if (values.length === headers.length) {
            const row = {};
            for (let j = 0; j < headers.length; j++) {
              row[headers[j]] = values[j];
            }
            data.push(row);
          }
        }
        this.handleData(data);
      };
    },
  },
  mounted() {
    const el = this.$el;
    el.addEventListener("dragenter", () => {
      el.classList.add("is-dragover");
    });
    el.addEventListener("dragleave", () => {
      el.classList.remove("is-dragover");
    });
    el.addEventListener("drop", (event) => {
      event.preventDefault();
      el.classList.remove("is-dragover");
      this.handleFileUpload(event);
    });
  },
};
</script>

<style scoped lang="scss">
.csv-upload {
  border: 2px dashed #ccc;
  padding: 20px;
  text-align: center;
  cursor: pointer;
  box-sizing: border-box;
  display: flex;
  align-items: center;
  justify-content: center;

  &:hover {
    background-color: #f0f0f0;
  }
}
.csv-upload.is-dragover {
  background-color: #f0f0f0;
}
</style>
