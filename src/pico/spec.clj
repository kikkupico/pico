(ns pico.spec
  (:require [pico.defs :refer :all])
  (:gen-class))

(def resources [ "todos" "teams"])

(specs
  [ Anyone can GET "shows"]
  [ AuthUser can [GET, POST] "tickets"])
