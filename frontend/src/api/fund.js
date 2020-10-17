import request from '@/utils/request'

export function fetchFundLog(query) {
  return request({
    url: '/log/fundlog/',
    method: 'get',
    params: query
  })
}

export function fetchFund(id) {
  return request({
    url: '/vue-element-admin/article/detail',
    method: 'get',
    params: { id }
  })
}

export function createFundLog(data) {
  return request({
    url: '/vue-element-admin/article/create',
    method: 'post',
    data
  })
}
