(ns pico.defs
  (:gen-class))
(require '[clojure.core.match :refer [match]])

(def Anyone :Anyone)
(def AuthUser :AuthUser)
(def can :can)
(def GET :GET)
(def POST :POST)

(defn parse-spec [s]
  (match s
    [p :can a r] [:resourcedef p a r ]
    :else :unknown))
(defn specs [a & b] (map parse-spec (cons a b)))
