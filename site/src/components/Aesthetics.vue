<template>
  <div class="aesthetics">
    <ul>
      <li v-for='tag in top10tags'>
        {{tag}}
      </li>
    </ul>
    <br/>
  </div>
</template>


<script>
// Here we can use ES6 (ES2015) features, like 'let'.
// console.log(this.$store)
// let top10tags = [$store.foo]
let top10tags = [1, 2, 3]
// TODO pick up here: figure out why $store isn't getting piped around. or how it is at all :-/
export default {
  data () {
    return {
      top10tags: top10tags
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>

