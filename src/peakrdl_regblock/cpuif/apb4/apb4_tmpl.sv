// Request
logic is_active;
wire is_activeVoted = is_active;
always_ff {{get_always_ff_event(cpuif.reset)}} begin
    is_active <= is_activeVoted;
    cpuif_req <= cpuif_reqVoted;
    cpuif_req_is_wr <= cpuif_req_is_wrVoted;
    cpuif_addr <= cpuif_addrVoted;
    cpuif_wr_data <= cpuif_wr_dataVoted;
    cpuif_wr_biten <= cpuif_wr_bitenVoted;
    if({{get_resetsignal(cpuif.reset)}}) begin
        is_active <= '0;
        cpuif_req <= '0;
        cpuif_req_is_wr <= '0;
        cpuif_addr <= '0;
        cpuif_wr_data <= '0;
        cpuif_wr_biten <= '0;
    end else begin
        if(~is_activeVoted) begin
            if({{cpuif.signal("psel")}}) begin
                is_active <= '1;
                cpuif_req <= '1;
                cpuif_req_is_wr <= {{cpuif.signal("pwrite")}};
                {%- if cpuif.data_width_bytes == 1 %}
                cpuif_addr <= {{cpuif.signal("paddr")}}[{{cpuif.addr_width-1}}:0];
                {%- else %}
                cpuif_addr <= { {{-cpuif.signal("paddr")}}[{{cpuif.addr_width-1}}:{{clog2(cpuif.data_width_bytes)}}], {{clog2(cpuif.data_width_bytes)}}'b0};
                {%- endif %}
                cpuif_wr_data <= {{cpuif.signal("pwdata")}};
                for(int i=0; i<{{cpuif.data_width_bytes}}; i++) begin
                    cpuif_wr_biten[i*8 +: 8] <= {8{ {{-cpuif.signal("pstrb")}}[i]}};
                end
            end
        end else begin
            cpuif_req <= '0;
            if(cpuif_rd_ackVoted || cpuif_wr_ackVoted) begin
                is_active <= '0;
            end
        end
    end
end

// Response
assign {{cpuif.signal("pready")}} = cpuif_rd_ackVoted | cpuif_wr_ackVoted;
assign {{cpuif.signal("prdata")}} = cpuif_rd_dataVoted;
assign {{cpuif.signal("pslverr")}} = cpuif_rd_errVoted | cpuif_wr_errVoted;
