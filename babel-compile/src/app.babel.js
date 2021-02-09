/**
 * Syslog DB View
 */
(function(){
    var facilities = {"KERN":0,"USER":1,"MAIL":2,"DAEMON":3,"AUTH":4,"SYSLOG":5,"LPR":6,"NEWS":7,"UUCP":8,"CRON":9,"AUTHPRIV":10,"FTP":11,"NTP":12,"SECURITY":13,"CONSOLE":14,"SOLARIS_CRON":15,"LOCAL0":16,"LOCAL1":17,"LOCAL2":18,"LOCAL3":19,"LOCAL4":20,"LOCAL5":21,"LOCAL6":22,"LOCAL7":23};
    var severitylevels = {"EMERG":0,"ALERT":1,"CRIT":2,"ERR":3,"WARNING":4,"NOTICE":5,"INFO":6,"DEBUG":7};
    function revKeyVal(i){var o={};Object.keys(i).forEach(k=>{o[i[k]]=k;});return o;}
    var facilities_str = revKeyVal(facilities);
    var severitylevels_str = revKeyVal(severitylevels);

    class FilterFacility extends React.Component {
        constructor(props){
            super(props);
            this.state = { checked: true }
        }
        toggleChange(t){
            t.setState(state => ({checked: !state.checked}));
        }
        render() {
            return <li><input type="checkbox" data-type="facility" value={this.props.value} defaultChecked={this.state.checked} onChange={(function(t){return function(){t.toggleChange(t)}})(this)}></input>{this.props.label}</li>
        }
    }
    class FilterSeverity extends React.Component{
        constructor(props){
            super(props);
            this.state = {checked: true}
        }
        toggleChange(){
            this.setState(state => ({checked: !state.checked}));
        }
        render(){
            return <li><input type="checkbox" data-type="severity" value={this.props.value} defaultChecked={this.state.checked} onChange={(function(t){return function(){t.toggleChange(t)}})(this)}></input>{this.props.label}</li>
        }
    }
    class FilterHost extends React.Component{
        constructor(props){
            super(props);
            this.state = {checked: true}
        }
        toggleChange(){
            this.setState(state => ({checked: !state.checked}));
        }
        render(){
            return <li><input type="checkbox" data-type="host" value={this.props.value} defaultChecked={this.state.checked} onChange={(function(t){return function(){t.toggleChange(t)}})(this)}></input>{this.props.label}</li>
        }
    }
    function generateFilter(){
        function FacilitiesFilter(props){
            const facility = props.facilities;
            // Generate facility
            var items = Object.keys(facility).map(function(key){
                return <FilterFacility key={"filter_facility_"+facility[key].toString()} value={facility[key]} label={key}></FilterFacility>
            });
            return <div>{"Facility"}<br></br><ul>{items}</ul></div>
        }
        
        ReactDOM.render(
            <FacilitiesFilter facilities={facilities}></FacilitiesFilter>,
            $("div.filter#facility")[0]);

        
        function SeverityFilter(props){
            const severity = props.severity;
            var items = Object.keys(severity).map(function(key){
                return <FilterSeverity key={"filter_severity_"+severity[key].toString()} value={severity[key]} label={key}></FilterSeverity>
            });
            return <div>{"Severity"}<br></br><ul>{items}</ul></div>
        }
        ReactDOM.render(
            <SeverityFilter severity={severitylevels}></SeverityFilter>,
            $("div.filter#severity")[0]
        )

        fetch("/cgi-bin/hosts").then(function(resp){
            resp.json().then(function(hosts){
                function HostFilter(props){
                    var items = props.hosts.map(function(host, idx){
                        return <FilterHost key={"filter_host_" + idx.toString()} value={host} label={host}></FilterHost>
                    });
                    return <div>{"Hosts"}<br></br><ul>{items}</ul></div>
                }
                ReactDOM.render(
                    <HostFilter hosts={hosts}></HostFilter>,
                    $("div.filter#hostname")[0]
                )
            });
        });
    }
    /**
     * Retrieve all filter values
     */
    function getFilter(){
        var sev = Array.from($("input[data-type=severity]")).filter(a => a.checked).map(a=>Number(a.value)).reduce(function(acc,curr){return acc | (0x01 << curr)}, 0);
        var fac = Array.from($("input[data-type=facility]")).filter(a => a.checked).map(a=>Number(a.value)).reduce(function(acc,curr){return acc | (0x01 << curr)}, 0);
        var hosts = Array.from($("input[data-type=host]")).filter(a => a.checked).map(a=>a.value);
        var ts = (new Date($("#filter_dtfrom")[0].value)).getTime();
        var tf = (new Date($("#filter_dtto")[0].value)).getTime();
        var out = new URLSearchParams();
        out.append("ts",ts);
        out.append("tf",tf);
        hosts.forEach(host=>out.append("host",host));
        out.append("nosev", sev);
        out.append("nofac", fac);
        return out;
    }
    class SyslogHeader extends React.Component {
        render(){
            return <tr>
                <th>{"Received Time"}</th>
                <th>{"Facility"}</th>
                <th>{"Severity"}</th>
                <th>{"Host"}</th>
                <th>{"Process"}</th>
                <th>{"Message"}</th>
            </tr>
        }
    }
    class Syslog extends React.Component {
        constructor(props){
            super(props);
        }
        render(){
            return <tr data-severity={this.props.data.PRI_SEVERITY}>
                <td>{(new Date(this.props.timestamp)).toLocaleString()}</td>
                <td>{facilities_str[this.props.data.PRI_FACILITY]}</td>
                <td>{severitylevels_str[this.props.data.PRI_SEVERITY]}</td>
                <td>{this.props.data.HEAD.hostname}</td>
                <td>{this.props.data.HEAD.process}</td>
                <td>{this.props.data.MSG}</td>
            </tr>
        }
    }
    function updateData(){
        fetch("/cgi-bin/list?"+getFilter().toString()).then(function(resp){
            resp.json().then(function(data){
                var outHtml = data.map(entry=>{
                    return <Syslog key={entry._id} data={entry.data} timestamp={entry.timestamp}></Syslog>
                });
                ReactDOM.render(
                    <table><tbody>
                        <SyslogHeader></SyslogHeader>
                        {outHtml}
                    </tbody></table>,
                    $("div.content")[0]);
            });
        });
    }
    generateFilter();
    updateData();
    $("#filter_apply_btn").on("click", updateData);
    $("#filter_updatehost_btn").on("click", generateFilter);
})()