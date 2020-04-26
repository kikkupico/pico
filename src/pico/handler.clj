(ns pico.handler
  (:require [compojure.core :refer :all]
            [compojure.route :as route]
            ; [ring.middleware.defaults :refer [wrap-defaults api-defaults]]
            [clojure.data.json :as json]
            [ring.middleware.json :refer [wrap-json-response wrap-json-body]]            
            [ring.util.response :refer [response]]
            [ring.util.request :refer [body-string]]
            [clojure.java.jdbc :as jdbc]
            [pico.persistence :refer :all]
            [pico.spec :refer :all]))

(defn rowToJson [r]
  (dissoc 
    (merge r
      (json/read-str (:properties r)))
    :properties))

(defn crud+ [url] 
  [ (GET (str "/" url) req
      (response
        (map rowToJson (jdbc/query db-spec [(str "SELECT * from " url )]))))
    (GET (str "/" url "/" ":id") [id]      
        (let [items (jdbc/query db-spec [(str "SELECT * from " url " where id = " id)])]          
          (if (empty? items)
            {:status 404 :body "Not found"}
            (response (first (map rowToJson items))))))
    (POST (str "/" url) req 
      (jdbc/insert! db-spec url {:properties (json/write-str (:body req))}) "OK")
    (PUT (str "/" url) req url)
    (DELETE (str "/" url) req url) ])

(defn make-routes [resources]
  (apply routes
    (into []
      (mapcat crud+ resources))))

(def dyn-routes (make-routes resources))

(def app
  (-> dyn-routes
      wrap-json-body
      wrap-json-response))

(println "Started server")
