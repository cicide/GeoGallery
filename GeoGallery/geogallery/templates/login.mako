<%inherit file="/base.mako" />
<%def name="title()">Login</%def>

<%block name="body_content">
        %if form:
          ${form|n}
        %endif
    <script type="text/javascript">
        deform.load()
    </script>
</%block>
