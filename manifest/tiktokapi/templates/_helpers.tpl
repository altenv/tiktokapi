{{- define "chart.fullname" -}}
{{- $name := default .Chart.Name .Values.nameOverride -}}
{{- printf "%s-%s" .Release.Namespace $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "chart.volume" -}}
{{- if .Values.configmap.enabled -}}{{ range .Values.configmap.configs }}
volumes:
- name: {{ include "chart.fullname" $ }}-{{ .file_name_app | replace "." "-" }}-volume
  configMap:
    name: {{ include "chart.fullname" $ }}-configmap
    items: 
    - key: {{ .file_name_app }}
      path: {{ .file_name_app }}
{{- end }}
{{- end -}}
{{- if .Values.gcs.enabled }}
- name: {{ include "chart.fullname" . }}-gcs-credential-volume
  secret:
    secretName: {{ .Values.gcs.serviceAccount }}
{{- end }}
{{- end -}}

{{- define "chart.volume.mount" -}}
{{- if .Values.configmap.enabled -}}
volumeMounts: {{ range .Values.configmap.configs }}
- mountPath: {{ $.Values.configmap.configPath }}/{{ .file_name_app }}
  subPath: {{ .file_name_app }}
  name: {{ include "chart.fullname" $ }}-{{ .file_name_app | replace "." "-" }}-volume
{{- end }}
{{- end -}}
{{- if .Values.pubsub.enabled }}
- mountPath: {{ .Values.configmap.configPath }}/{{ .Values.pubsub.filename }}
  subPath: {{ .Values.pubsub.filename }}
  name: {{ include "chart.fullname" . }}-pubsub-credential-volume
{{- end }}
{{- if .Values.gcs.enabled }}
- mountPath: {{ .Values.configmap.configPath }}/{{ .Values.gcs.filename }}
  subPath: {{ .Values.gcs.filename }}
  name: {{ include "chart.fullname" . }}-gcs-credential-volume
{{- end }}
{{- end -}}
