<script setup>
import { computed, onBeforeMount, ref } from "vue";
import axios from "axios";
import _ from "lodash";
</script>

<template>
  <div class="container-fluid">
    <div style="background: #f4f4ff; margin: 40px 180px 40px 180px">
      <div class="row" style="padding-bottom: 10px">
        <div class="col-auto">
          <select class="form-select">
            <option>Заглавие/Название</option>
            <option>Автор</option>
          </select>
        </div>
        <div class="col">
          <input type="text" class="form-control" />
        </div>
      </div>
      <div class="row" style="padding-bottom: 10px">
        <div class="col-auto">
          <select class="form-select">
            <option>И</option>
            <option>ИЛИ</option>
          </select>
        </div>
      </div>
      <div class="row" style="padding-bottom: 10px">
        <div class="col-auto">
          <select class="form-select">
            <option>Автор</option>
            <option>Заглавие/Название</option>
          </select>
        </div>
        <div class="col">
          <input type="text" class="form-control" />
        </div>
      </div>
      <div class="row" style="padding-bottom: 10px">
        <div class="col-auto">
          <button type="button" class="btn btn-primary">
            Добавить условие <i class="bi bi-plus-square"></i>
          </button>
        </div>
      </div>
      <div class="row" style="justify-content: center">
        <div class="col-auto">
          <button type="button" class="btn btn-primary">
            Поиск <i class="bi bi-search"></i>
          </button>
        </div>
      </div>
    </div>
    <div>
      <div class="card" style="width: 18rem">
        <img src="..." class="card-img-top" alt="..." />
        <div class="card-body">
          <h5 class="card-title">Название книги</h5>
          <h6 class="card-title">Автор книги</h6>
          <button class="btn btn-info" type="button">
            <i class="bi bi-cart3"></i>
          </button>
          <p class="card-text">3шт</p>
        </div>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
</style>