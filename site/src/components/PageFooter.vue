<!-- This is a "single file component"; more info at:
    http://vuejs.org/guide/single-file-components.html-->

<template>
  <div class="page-footer">
    <!-- I guess "footer" is an HTML reserved word -->
    Neighborhood Guides is made by <a href="http://www.dantasse.com">Dan Tasse</a> and collaborators at the <a href="https://www.hcii.cmu.edu/">CMU HCII</a> <a href="http://www.cmuchimps.org/">CHIMPS Lab.</a> We welcome feedback at dantasse@cmu.edu.
  </div>
</template>

<script>
export default {
  components: {

  },
  data () {
    return {
    }
  }
}

</script>

<style scoped>

.page-footer {
  width: 100%;
  background: #ccc;
  padding: 20px;
  margin: 10px 0;
}
</style>

