{{- define "iperf3-chart.fullname" -}}
{{- printf "%s-%s" .Release.Name .Chart.Name -}}
{{- end -}}

{{- define "iperf3-chart.server.fullname" -}}
{{- printf "%s-server" (include "iperf3-chart.fullname" .) -}}
{{- end -}}

{{- define "iperf3-chart.client.fullname" -}}
{{- printf "%s-client" (include "iperf3-chart.fullname" .) -}}
{{- end -}}

