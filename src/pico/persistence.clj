(ns pico.persistence
  (:require
    [clojure.java.jdbc :as jdbc]
    [pico.spec :refer :all])
  (:gen-class))

(def db-spec
  {:classname   "org.sqlite.JDBC"
   :subprotocol "sqlite"
   :subname     "db/database.db"
   })


(def tables
  (jdbc/with-db-metadata [md db-spec]
    (into [] 
      (map :table_name 
        (jdbc/metadata-result (.getTables md nil nil nil (into-array ["TABLE" "VIEW"])))))))


(defn make-table [name]
  (let 
    [cmd
      (jdbc/create-table-ddl name 
        [ [:id :integer :primary :key]
          [:properties :text]
          [:creator :integer] 
          [:created_at :timestamp "default (strftime('%s', 'now'))"]])]
    (jdbc/db-do-commands db-spec [cmd])))


(defn setup []   
  (doseq [ r resources]
    (println (str "Creating table " r))
    (if (not (.contains tables r))
      (make-table r))))
