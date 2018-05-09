'use strict';

module.exports = (sequelize, DataTypes) => {
  var Model = sequelize.define('checkin_checkinevent', {
    'check_in_group_id': {
      type: DataTypes.INTEGER,
    },
  }, {
    tableName: 'checkin_checkinevent',
    underscored: true,
    timestamps: false,
    
  });

  Model.associate = (models) => {
  };

  return Model;
};

